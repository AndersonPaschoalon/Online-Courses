import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import fashion_mnist
import tensorflow as tf
from tensorflow.keras import layers


def create_autoencoder(latent_dim):
    # Define encoder layers
    encoder_inputs = tf.keras.Input(shape=(28, 28))
    flatten_layer = layers.Flatten()(encoder_inputs)
    encoder_outputs = layers.Dense(latent_dim, activation='relu')(flatten_layer)
    encoder = tf.keras.Model(encoder_inputs, encoder_outputs)

    # Define decoder layers
    decoder_inputs = tf.keras.Input(shape=(latent_dim,))
    decoder_dense_layer = layers.Dense(784, activation='sigmoid')(decoder_inputs)
    decoder_outputs = layers.Reshape((28, 28))(decoder_dense_layer)
    decoder = tf.keras.Model(decoder_inputs, decoder_outputs)

    # Combine encoder and decoder into autoencoder
    autoencoder_inputs = tf.keras.Input(shape=(28, 28))
    encoded = encoder(autoencoder_inputs)
    decoded = decoder(encoded)
    autoencoder = tf.keras.Model(autoencoder_inputs, decoded)

    return autoencoder

def load_fashion_mnist():
    (x_train, _), (x_test, _) = fashion_mnist.load_data()

    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.

    print(x_train.shape)
    print(x_test.shape)

    return x_train, x_test


def main():
    x_train, x_test = load_fashion_mnist()
    latent_dim = 64
    autoencoder = create_autoencoder(latent_dim)
    #autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())
    autoencoder.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    autoencoder.fit(x_train, x_train,
                    epochs=10,
                    shuffle=True,
                    validation_data=(x_test, x_test))
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
    plt.savefig(".\\Results\\11\\tf2FuncApi_FsshionMnist_original_vs_reconstructed")


if __name__ == '__main__':
    main()

