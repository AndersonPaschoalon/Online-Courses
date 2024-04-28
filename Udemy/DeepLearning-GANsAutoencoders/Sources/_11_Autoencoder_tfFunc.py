# https://www.tensorflow.org/tutorials/generative/autoencoder?hl=pt-br

import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras import layers
from tensorflow.keras import layers, losses

OUT_PATH = ".\\Results\\11\\"
epochs = 50


class AutoencoderFactory:

    def __init__(self,
               input_shape=(28, 28),
               latent_dim=64,
               optimizer='adam',
               loss=losses.MeanSquaredError()):
        flattened_dim = input_shape[0]*input_shape[1]
        # Define encoder layers
        ei = tf.keras.Input(shape=input_shape)
        ex = layers.Flatten()(ei)
        ex = layers.Dense(latent_dim, activation='relu')(ex)
        #encoder = tf.keras.Model(ei, ex)

        # Define decoder layers
        #di = tf.keras.Input(shape=(latent_dim,))
        dx = layers.Dense(flattened_dim, activation='sigmoid')(ex)
        dx = layers.Reshape((input_shape[0], input_shape[1]))(dx)
        #self.decoder = tf.keras.Model(di, dx)

        # Combine encoder and decoder into autoencoder
        self.autoencoder = tf.keras.Model(ei, dx)
        self.autoencoder.compile(optimizer=optimizer, loss=loss)


def load_fashion_mnist():
    (x_train, _), (x_test, _) = fashion_mnist.load_data()
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    print(x_train.shape)
    print(x_test.shape)
    return x_train, x_test


def plot_cost_function(history):
    # Plot cost function over iterations
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Cost Function Over Iterations')
    plt.legend()
    plot_file = os.path.join(OUT_PATH, "tf2_FuncApi_FashionMnist_CostFunction")
    plt.savefig(plot_file)


def main():
    x_train, x_test = load_fashion_mnist()
    input_shape = x_train[0].shape
    af = AutoencoderFactory(input_shape=input_shape,
                            latent_dim=64,
                            optimizer='adam',
                            loss=losses.MeanSquaredError())
    history = af.autoencoder.fit(x_train,
                                 x_train,
                                 epochs=50,
                                 shuffle=True,
                                 validation_data=(x_test, x_test))
    plot_cost_function(history)
    decoded_imgs = af.autoencoder(x_test).numpy()
    n = 10
    plt.clf()
    plt.figure(figsize=(20, 4))
    for i in range(n):
        # display original
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(x_test[i])
        plt.title("original")
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # display reconstruction
        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded_imgs[i])
        plt.title("reconstructed")
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    # plt.show()
    plot_file = os.path.join(OUT_PATH, "tf2_FuncApi_FashionMnist_OriginalVsReconstructed")
    plt.savefig(plot_file)


if __name__ == '__main__':
    main()

