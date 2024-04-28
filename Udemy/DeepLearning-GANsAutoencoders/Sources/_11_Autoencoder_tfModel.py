# https://www.tensorflow.org/tutorials/generative/autoencoder?hl=pt-br
from keras.backend import learning_phase

import util
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model


OUT_PATH = ".\\Results\\11\\"
epochs = 50


class Autoencoder(Model):

    def __init__(self, latent_dim):
      super(Autoencoder, self).__init__()
      self.latent_dim = latent_dim
      # encoder: simple NPL, compress using a fully connected NPL
      self.encoder = tf.keras.Sequential([
          layers.Flatten(),
          layers.Dense(self.latent_dim, activation='relu'),
      ])
      # decode back to a 28x28 matrix
      self.decoder = tf.keras.Sequential([
          layers.Dense(784, activation='sigmoid'),
          layers.Reshape((28, 28))
      ])

    def call(self, x):
      encoded = self.encoder(x)
      decoded = self.decoder(encoded)
      return decoded


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
    plot_file = os.path.join(OUT_PATH, "tf2_ModelApi_FashionMnist_CostFunction")
    plt.savefig(plot_file)


def main():
    x_train, x_test = load_fashion_mnist()
    latent_dim = 64
    autoencoder = Autoencoder(latent_dim)
    autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())
    # autoencoder.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    history = autoencoder.fit(x_train,
                              x_train,
                              epochs=epochs,
                              shuffle=True,
                              validation_data=(x_test, x_test))
    plot_cost_function(history)
    encoded_imgs = autoencoder.encoder(x_test).numpy()
    decoded_imgs = autoencoder.decoder(encoded_imgs).numpy()
    n = 10
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
    plot_file = os.path.join(OUT_PATH, "tf2_ModelApi_FashionMnist_OriginalVsReconstructed")
    plt.savefig(plot_file)


if __name__ == '__main__':
    main()



