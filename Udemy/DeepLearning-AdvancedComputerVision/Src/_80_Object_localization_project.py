import os
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import SGD
from matplotlib.patches import Rectangle


def image_generator(batch_size=64):
    # gerar imagens e targets
    while True:
    # cada epoca ira ter 50 batches, sem nenhuma razao especifica
        for _ in range(50):
            # tamanho do batch, altura, lartura, cor
            img_batch_dimensions = (batch_size, 100, 100, 3)
            # tamanho do batch, coordenadas para se definir a caixa
            target_dimensions = (batch_size, 4)
            X = np.zeros(img_batch_dimensions)
            Y = np.zeros(target_dimensions)
            
            for i in range(batch_size):
                # construir as caixas, e armazenar suas localizações nos targets
                row0 = np.random.randint(90)
                col0 = np.random.randint(90)
                row1 = np.random.randint(row0, 100)
                col1 = np.random.randint(col0, 100)
                # construir imagem
                X[i, row0:row1, col0:col1, :] = 1
                # construir targets
                Y[i, 0] = row0/100
                Y[i, 1] = col0/100
                Y[i, 2] = (row1 - row0)/100
                Y[i, 3] = (col1 - col0) / 100
            # faz a função operar como um gerador
            yield X, Y


def _test_image_generator():
    img_batch = image_generator()
    for img in img_batch:
        X, Y = img
        print("X[0]:", X[0, :, :, 0])
        print("Y[0]:", Y[0])
        plt.imshow(X[0, :, :, :])
        plt.show()
        break


def make_prediction(model, out_dir, pred_id):
    # generate random image
    x = np.zeros((100, 100, 3))
    row0 = np.random.randint(90)
    col0 = np.random.randint(90)
    row1 = np.random.randint(row0, 100)
    col1 = np.random.randint(col0, 100)
    x[row0:row1, col0:col1, :] = 1
    print(f"row0:{row0}, col0:{col0}, row1:{row1}, col1:{col1}")

    # Predict
    X = np.expand_dims(x, 0)
    p = model.predict(X)[0]

    # draw the box
    fig, ax = plt.subplots(1)
    ax.imshow(x)
    rect = Rectangle(
        (p[1]*100, p[0]*100),
        p[3]*100,
        p[2]*100,
        linewidth=1,
        edgecolor='r',
        facecolor='none'
    )
    ax.add_patch(rect)
    plt.savefig(os.path.join(out_dir, f"test_prediction_{pred_id}"))


def main():
        # transfer leaning - utilizar uma rede pre-treinada para implementar a estimativa
        vgg = tf.keras.applications.VGG16(input_shape=[100, 100, 3],
                                          # tamanho da imagem, altura 100, largura 100, 3 canais de cores, vgg trabalha com imagens coloridas
                                          include_top=False,
                                          # utilizar parametros pre-treinados da rede, será treinada somente a cabeça
                                          weights='imagenet') # utilizar pesos treinados na imagenet
        # hyperparameters
        hp_adam_lr = 0.001
        # hp_steps_epoch = 50
        hp_steps_epoch = 5
        hp_epochs = 5
        out_dir = "80"

        # build the model
        x = Flatten()(vgg.output)
        x = Dense(4, activation='sigmoid')(x)
        model = Model(vgg.input, x)

        # compile the model
        model.compile(loss='binary_crossentropy', optimizer=Adam(lr=hp_adam_lr))

        # fit the model
        model.fit_generator(image_generator(),
                            steps_per_epoch=hp_steps_epoch,
                            epochs=hp_epochs)

        # make prediction
        for i in range(10):
            make_prediction(model, out_dir, pred_id=i)




if __name__ == '__main__':
    # tf.config.threading.set_inter_op_parallelism_threads(1)
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    print(tf.__version__)
    run_main = True
    test01 = False

    if run_main:
        main()
    if test01:
        _test_image_generator()



