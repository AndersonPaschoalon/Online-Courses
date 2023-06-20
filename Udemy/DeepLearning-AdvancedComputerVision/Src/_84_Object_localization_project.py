import os
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import SGD
# from tensorflow.keras.processing import image
from matplotlib.patches import Rectangle
from imageio import imread


OUT_DIR = "84"


def pokemon_generator(pokemon_img="84/charmander-tight.png", image_dim=200, batch_size=64):
    # carregar charmander
    ch = imread(pokemon_img)
    CH_H, CH_W, _, = ch.shape
    print(f"- {pokemon_img} shape:{ch.shape}")
    POKE_DIM = image_dim
    # gerar imagens e targets
    while True:
    # cada epoca ira ter 50 batches, sem nenhuma razao especifica
        for _ in range(50):
            # tamanho do batch, altura, lartura, cor
            img_batch_dimensions = (batch_size, POKE_DIM, POKE_DIM, 3)
            # tamanho do batch, coordenadas para se definir a caixa
            target_dimensions = (batch_size, 4)
            X = np.zeros(img_batch_dimensions)
            Y = np.zeros(target_dimensions)
            
            for i in range(batch_size):
                # calcular localização do charmander
                row0 = np.random.randint(POKE_DIM - CH_H)
                col0 = np.random.randint(POKE_DIM - CH_W)
                row1 = row0 + CH_H
                col1 = col0 + CH_W
                # inserir o charmander na imagem
                X[i, row0:row1, col0:col1, :] = ch[:, :, :3]
                # construir targets
                Y[i, 0] = row0/POKE_DIM
                Y[i, 1] = col0/POKE_DIM
                Y[i, 2] = (row1 - row0)/POKE_DIM
                Y[i, 3] = (col1 - col0)/POKE_DIM

            # faz a função operar como um gerador
            X_yield = X/255.0
            yield X/255.0, Y


def _test_image_generator(save_name=""):
    img_batch = pokemon_generator()
    for img in img_batch:
        X, Y = img
        print("X[0]:", X[0, :, :, 0])
        print("Y[0]:", Y[0, :])
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
    x = Dense(4, activation='sigmoid')(x)
    model = Model(vgg.input, x)

    # compile the model
    model.compile(loss='binary_crossentropy', optimizer=Adam(lr=hp_adam_lr))

    return model


def pokemon_prediction(model, out_dir, pred_id, poke_dim, poke_h, poke_w):
    # generate random image
    x = np.zeros((poke_dim, poke_dim, 3))
    row0 = np.random.randint(poke_dim - poke_h)
    col0 = np.random.randint(poke_dim - poke_w)
    row1 = row0 - poke_h
    col1 = col0 - poke_w
    x[row0:row1, col0:col1, :] = 1
    print(f"row0:{row0}, col0:{col0}, row1:{row1}, col1:{col1}")

    # Predict
    X = np.expand_dims(x, 0) / 255
    p = model.predict(X)[0]

    # calculate target/loss
    y = np.zeros(4)
    y[0] = row0/poke_dim
    y[1] = col0 / poke_dim
    y[2] = (row1 - row0) / poke_dim
    y[3] = (col1 - col0) / poke_dim

    # draw the box
    row0 = int(p[0]*poke_dim)
    col0 = int(p[1]*poke_dim)
    row1 = int(row0 + p[2]*poke_dim)
    col1 = int(col0 + p[3]*poke_dim)
    print(f"pred: {row0}, {col0}. {row1}. {col1}")
    print(f"loss: { -np.mean( y*np.log(p) + (1 - y)*np.log(1 - p) )}")

    fig, ax = plt.subplots(1)
    ax.imshow(x.astype(np.uint8))
    rect = Rectangle(
        (p[1]*poke_dim, p[0]*poke_dim),
        p[3]*poke_dim,
        p[2]*poke_dim,
        linewidth=1,
        edgecolor='r',
        facecolor='none'
    )
    ax.add_patch(rect)
    plt.savefig(os.path.join(out_dir, f"test_prediction_{pred_id}"))


def main(fast=True):
        # load the pokemon
        poke_dim = 200
        pokemon_img = "84/charmander-tight.png"
        ch = imread(pokemon_img)
        ch_h, ch_w, _, = ch.shape
        print("pokemon shape:", ch.shape)

        # hyperparameters
        hp_adam_lr = 0.001
        hp_steps_epoch = 1
        hp_epochs = 5
        if not fast:
            hp_adam_lr = 0.0005
            hp_steps_epoch = 100
            hp_epochs = 10

        print("# build the model")
        model = make_model(img_h=poke_dim, img_w=poke_dim, hp_adam_lr=hp_adam_lr)

        print("# test generator")
        _test_image_generator(os.path.join(OUT_DIR, "test_img_generator"))

        print("# fit the model")
        model.fit_generator(pokemon_generator(),
                            steps_per_epoch=hp_steps_epoch,
                            epochs=hp_epochs)

        print("# make prediction")
        for i in range(10):
            pokemon_prediction(model, OUT_DIR, pred_id=i, poke_dim=poke_dim, poke_h=ch_h, poke_w=ch_w)


if __name__ == '__main__':
    # tf.config.threading.set_inter_op_parallelism_threads(1)
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    config = tf.ConfigProto()
    config.gpu_options.visible_device_list = "0"
    session = tf.Session(config=config)

    print(tf.__version__)
    run_main = True
    test01 = False

    if run_main:
        main()
    if test01:
        _test_image_generator(save_name=os.path.join(OUT_DIR, "test_charmander"))



