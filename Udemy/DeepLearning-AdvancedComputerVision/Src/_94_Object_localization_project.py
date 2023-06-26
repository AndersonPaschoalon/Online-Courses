import os
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.layers import Flatten, Dense, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing import image
from matplotlib.patches import Rectangle
from imageio import imread
import shutil
from skimage.transform import resize
from glob import glob
from tensorflow.keras.losses import binary_crossentropy, categorical_crossentropy


OUT_DIR = "94"


class PokeDic:

    def __init__(self, directory="94"):
        self.poke_dim = 200
        self.ch_file = os.path.join(directory, "pokemon/charmander-tight.png")
        self.bb_file = os.path.join(directory, "pokemon/bulbasaur-tight.png")
        self.sq_file = os.path.join(directory, "pokemon/squirtle-tight.png")
        ch = imread(self.ch_file)
        bb = imread(self.bb_file)
        sq = imread(self.sq_file)
        ch_h, ch_w, ch_c = ch.shape
        bb_h, bb_w, bb_c = bb.shape
        sq_h, sq_w, sq_c = sq.shape
        self.poke_data = [
            [ch, ch_h, ch_w, ch_c],
            [bb, bb_h, bb_w, bb_c],
            [sq, sq_h, sq_w, sq_c],
        ]
        self.class_names = ["Charmander", "Bulbasaur", "Squirtle"]


def config_tf():
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    gpus = tf.config.list_physical_devices('GPU')
    physical_devices = tf.config.list_physical_devices('GPU')
    try:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    except Exception as e:
        # Invalid device or cannot modify virtual devices once initialized.
        print(e)
        pass
    print(tf.__version__)


def pokemon_generator(poke_dic: PokeDic, batch_size=64):
    # load backgorunds
    backgrounds = load_backgrounds()
    poke_dim = poke_dic.poke_dim
    # gerar imagens e targets
    while True:
        # cada epoca ira ter 50 batches, sem nenhuma razao especifica
        for _ in range(50):
            # tamanho do batch, altura, lartura, cor
            X = np.zeros((batch_size, poke_dim, poke_dim, 3))
            # tamanho do batch, coordenadas para se definir a caixa
            # agora a output deve ter 5 variaveis
            Y = np.zeros((batch_size, 8))
            
            for i in range(batch_size):
                # select a random background
                bg_idx = np.random.choice(len(backgrounds))
                bg = backgrounds[bg_idx]
                bg_h, bg_w, _, = bg.shape
                rnd_h = np.random.randint(bg_h - poke_dim)
                rnd_w = np.random.randint(bg_w - poke_dim)
                X[i] = bg[rnd_h:rnd_h+poke_dim, rnd_w:rnd_w+poke_dim].copy()

                # 25% no object
                # 75% para as 3 classes
                appear = (np.random.random() < 0.75)
                if appear:
                    # choose a pokemon
                    pk_idx = np.random.randint(3)
                    pk, h, w, _ = poke_dic.poke_data[pk_idx]

                    # resize pokemon - make it bigger or smaller
                    scale = 0.5 + np.random.random() # 0.5 - 1.5
                    new_height = int(h * scale)
                    new_width = int(w * scale)
                    obj = resize(pk,
                                 (new_height, new_width),
                                 preserve_range=True).astype(np.uint8) # keep it from 0 - 255

                    # maybe flip
                    if np.random.random() < 0.5:
                        obj = np.fliplr(obj)

                    # calcular localização do charmander
                    row0 = np.random.randint(poke_dim - new_height)
                    col0 = np.random.randint(poke_dim - new_width)
                    row1 = row0 + new_height
                    col1 = col0 + new_width

                    # cant just assign obj to a slice of X
                    # since the transparent parts will be black (0)
                    mask = (obj[:, :, 3] == 0) # find where the pokemon is zero
                    bg_slice = X[i, row0:row1, col0:col1, :] # where we want to place obj
                    bg_slice = np.expand_dims(mask, -1) * bg_slice # (h, w, 1) x (h, w, 3)
                    bg_slice += obj[:, :, :3] # add the pokemon to the slice
                    X[i, row0:row1, col0:col1, :] = bg_slice # put the slice back
                    # # inserir o charmander na imagem
                    # X[i, row0:row1, col0:col1, :] = obj[:, :, :3]

                    # construir targets

                    # location
                    Y[i, 0] = row0/poke_dim
                    Y[i, 1] = col0/poke_dim
                    Y[i, 2] = (row1 - row0)/poke_dim
                    Y[i, 3] = (col1 - col0)/poke_dim

                    # class
                    Y[i, 4 + pk_idx] = 1 # as outras serão zero

                # o pokemon apareceu?
                Y[i, 7] = appear

            # faz a função operar como um gerador
            X_yield = X/255.0
            yield X_yield, Y


def _test_image_generator(save_name=""):
    poke_dic = PokeDic(directory=OUT_DIR)
    img_batch = pokemon_generator(poke_dic=poke_dic)
    for img in img_batch:
        X, Y = img
        print(f"X.shape:{X.shape}, X[0, :, :, 0]:{X[0, :, :, 0]}")
        print(f"Y.shape:{Y.shape}, Y[0]:{Y[0, :]}")
        plt.imshow(X[0, :, :, :])
        if save_name == "":
            plt.show()
        else:
            plt.savefig(save_name)
        break


def make_model(img_h, img_w, hp_adam_lr):
    # transfer leaning - utilizar uma rede pre-treinada para implementar a estimativa
    vgg = tf.keras.applications.VGG16(input_shape=[img_h, img_w, 3],
                                      # tamanho da imagem, altura 100, largura 100, 3 canais de cores, vgg trabalha com imagens coloridas
                                      include_top=False,
                                      # utilizar parametros pre-treinados da rede, será treinada somente a cabeça
                                      weights='imagenet')  # utilizar pesos treinados na imagenet

    # build the model
    x = Flatten()(vgg.output)

    # localizador
    x1 = Dense(4, activation='sigmoid')(x)
    # classe do objeto
    x2 = Dense(3, activation='softmax')(x)
    # objeto apareceu ou não
    x3 = Dense(1, activation='sigmoid')(x)

    x = Concatenate()([x1, x2, x3])
    model = Model(vgg.input, x)

    # compile the model
    model.compile(loss=custom_loss, optimizer=Adam(lr=hp_adam_lr))

    return model


def pokemon_prediction(model, out_dir, pred_id, poke_dic: PokeDic):
    print("")
    print("#############################################################")
    print("# Prediction ", pred_id)
    print("#############################################################")

    poke_dim = poke_dic.poke_dim

    # load backgrounds
    backgrounds = load_backgrounds()

    # select a random background
    bg_idx = np.random.choice(len(backgrounds))
    bg = backgrounds[bg_idx]
    bg_h, bg_w, _, = bg.shape
    rnd_h = np.random.randint(bg_h - poke_dim)
    rnd_w = np.random.randint(bg_w - poke_dim)
    x = np.zeros((poke_dim, poke_dim, 3))
    x = bg[rnd_h:rnd_h + poke_dim, rnd_w:rnd_w + poke_dim].copy()

    appear = (np.random.random() < 0.75)
    if appear:
        # load the pokemon image
        pk_idx = np.random.randint(3)
        pk, h, w, _ = poke_dic.poke_data[pk_idx]

        # resize pokemon
        scale = 0.5 + np.random.random()  # 0.5 - 1.5
        new_height = int(h * scale)
        new_width = int(w * scale)
        obj = resize(pk,
                     (new_height, new_width),
                     preserve_range=True).astype(np.uint8)  # keep it from 0 - 255

        # maybe flip
        if np.random.random() < 0.5:
            obj = np.fliplr(obj)

        # choose a random location to store the object
        row0 = np.random.randint(poke_dim - new_height)
        col0 = np.random.randint(poke_dim - new_width)
        row1 = row0 + new_height
        col1 = col0 + new_width
        print(f"poke_dim:{poke_dim}, x.shape:{x.shape}, row0:{row0}, col0:{col0}, row1:{row1}, col1:{col1}")

        # cant just assign obj to a slice of X
        # since the transparent parts will be black (0)
        mask = (obj[:, :, 3] == 0)  # find where the pokemon is zero
        bg_slice = x[row0:row1, col0:col1, :]  # where we want to place obj
        bg_slice = np.expand_dims(mask, -1) * bg_slice  # (h, w, 1) x (h, w, 3)
        bg_slice += obj[:, :, :3]  # add the pokemon to the slice
        x[row0:row1, col0:col1, :] = bg_slice  # put the slice back
        actual_class = poke_dic.class_names[pk_idx]
        print("true:", row0, col0, row1, col1, actual_class)

    # Predict
    X = np.expand_dims(x, 0) / 255
    p = model.predict(X)[0]

    # draw the box
    row0 = int(p[0]*poke_dim)
    col0 = int(p[1]*poke_dim)
    row1 = int(row0 + p[2]*poke_dim)
    col1 = int(col0 + p[3]*poke_dim)
    class_pred_idx = np.argmax(p[4:7])
    class_pred = poke_dic.class_names[class_pred_idx]

    # plot
    fig, ax = plt.subplots(1)
    ax.imshow(x.astype(np.uint8))

    # draw the box:
    if p[-1] > 0.5:
        print(f"p[4]:{p[4]}")
        rect = Rectangle(
            (p[1]*poke_dim, p[0]*poke_dim),
            p[3]*poke_dim,
            p[2]*poke_dim,
            linewidth=1,
            edgecolor='r',
            facecolor='none'
        )
        ax.add_patch(rect)
        print("Pred: ", row0, col0, col1, col1, class_pred)
    else:
        print("No object detected")
    plt.savefig(os.path.join(out_dir, f"test_prediction_{pred_id}"))


def _test_background():
    backgrounds = load_backgrounds()
    print(f"backgrounds.len: {len(backgrounds)}")
    plt.imshow(backgrounds[0])
    plt.show()


def load_backgrounds():
    backgrounds = []
    background_files = glob(os.path.join(OUT_DIR, "backgrounds/*.jpg"))
    for f in background_files:
        # ps: os backgroudns podem ter tamanhos diferentes
        bg = np.array(image.load_img(f))
        backgrounds.append(bg)
    return backgrounds


def custom_loss(y_true, y_pred):
    # target is a 5-tuple
    # (row, col, depth, width, object_appeared)
    # bce para as primeiras 4 colunas, ou seja sobre a caixa
    bce = binary_crossentropy(y_true[:, :4], y_pred[:, :4]) # location
    # qual o pokemon que apareceu
    cce = categorical_crossentropy(y_true[:, 4:7], y_pred[:, 4:7])
    # bce sobre se o objeto está ou não na imagem
    bce2 = binary_crossentropy(y_true[:, -1], y_pred[:, -1])

    return bce*y_true[:, -1] + cce * y_true[:, -1] + 0.5*bce2


def main(fast=True, delete_model=False):
        # load the pokemon
        model_file = os.path.join(OUT_DIR, "vgg16_pokemon.mod")

        # pokemon data
        poke_dic = PokeDic(directory=OUT_DIR)

        # hyperparameters - para performar bem, usar uma lr menor
        hp_adam_lr = 0.0001
        hp_steps_epoch = 1
        hp_epochs = 2
        if not fast:
            hp_adam_lr = 0.0001
            hp_steps_epoch = 100
            hp_epochs = 10

        if delete_model and os.path.exists(model_file):
            shutil.rmtree(model_file)

        if not os.path.exists(model_file):
            print("# build the model")
            model = make_model(img_h=poke_dic.poke_dim, img_w=poke_dic.poke_dim, hp_adam_lr=hp_adam_lr)

            print("# test generator")
            _test_image_generator(os.path.join(OUT_DIR, "test_img_generator"))

            print("# fit the model")
            model.fit_generator(pokemon_generator(poke_dic=poke_dic, batch_size=16),
                                steps_per_epoch=hp_steps_epoch,
                                epochs=hp_epochs)
            model.save(model_file)
        else:
            model = tf.keras.models.load_model(model_file,
                                               custom_objects={'custom_loss': custom_loss})

        print("# make prediction")
        for i in range(30):
            pokemon_prediction(model, OUT_DIR, pred_id=i, poke_dic=poke_dic)


if __name__ == '__main__':
    config_tf()
    run_main = True
    test01 = False
    test02 = False

    if run_main:
        main(fast=False, delete_model=True)
    if test01:
        _test_image_generator(save_name=os.path.join(OUT_DIR, "test_pokemon"))
    if test02:
        _test_background()



