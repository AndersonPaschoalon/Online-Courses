# https://www.kaggle.com/code/yvtsanlevy/introduction-to-generative-adversarial-network/notebook
import tensorflow as tf
keras = tf.keras

from keras.layers import Input, Dense, LeakyReLU, Dropout, BatchNormalization
from keras.models import Model
from keras.optimizers import SGD, Adam

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os


OUT_DIR = "76"

def load_mnist_dataset():
    # load the data from tensorflow
    mnist = keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    print("Mnist dataset: x_train.shape:", x_train.shape, ", y_train.shape:", y_train.shape, ", x_test.shape:", x_test.shape, ", y_test.shape:", y_test.shape)

    # plot some image
    plt.clf()
    print("y_train:", y_train[0])
    plt.imshow(x_train[0])
    sample_file = os.path.join(OUT_DIR, "mnist_sample_" + str(y_train[0]) )
    plt.savefig(sample_file)

    # scale the image
    # map inputs to (-1, +1) for better training
    x_train, x_test = x_train/255.0 * 2 - 1, x_test/155.0 * 2 - 1

    # flatten the data -> transform the data into a vector
    print("Old Array Dimensions: x_train.shape:", x_train.shape)
    print("Old Array Dimensions: x_test.shape:", x_test.shape)
    N, H, W = x_train.shape
    D = H*W  # data vector dimension
    x_train = x_train.reshape(-1, D)
    x_test = x_test.reshape(-1, D)
    print("New Array Dimensions: x_train.shape:", x_train.shape)
    print("New Array Dimensions: x_test.shape:", x_test.shape)

    # pre-processed and flattened output
    return D, N, H, W, (x_train, y_train), (x_test, y_test)


def build_generator(latent_dim, params, input_dimension):
    print("latent_dim: ", latent_dim)
    print("params: ", params)
    print("input_dimension: ", input_dimension)

    i = Input(shape=(latent_dim,))

    # L1
    x = Dense(params['l1'], activation=LeakyReLU(alpha=params['alpha-l1']))(i)
    x = BatchNormalization(momentum=params['bn1-momentum'])(x)

    # L2
    x = Dense(params['l2'], activation=LeakyReLU(alpha=params['alpha-l2']))(x)
    x = BatchNormalization(momentum=params['bn1-momentum'])(x)

    # L3
    x = Dense(params['l3'], activation=LeakyReLU(alpha=params['alpha-l3']))(x)
    x = BatchNormalization(momentum=params['bn3-momentum'])(x)

    # output
    x = Dense(input_dimension, activation=params['activation'])(x)

    model = Model(i, x)
    model.summary()
    return model


def generator_params():
    # dimensionality of the latent space
    latent_dim = 100

    params = dict()

    params['alpha-l1'] = 0.2
    params['alpha-l2'] = 0.2
    params['alpha-l3'] = 0.2

    params['l1'] = 256
    params['l2'] = 512
    params['l3'] = 1024

    params['bn1-momentum'] = 0.8
    params['bn2-momentum'] = 0.8
    params['bn3-momentum'] = 0.8

    params['activation'] = 'tanh'

    return latent_dim, params


def build_discriminator(img_size, params):
    print("img_size: ", img_size)
    print("params: ", params)
    i = Input(shape=(img_size,))
    x = Dense(params['l1'], activation=LeakyReLU(alpha=params['alpha-l1']))(i)
    x = Dense(params['l2'], activation=LeakyReLU(alpha=params['alpha-l2']))(x)
    x = Dense(params['l3'], activation=params['activation'])(x)
    model = Model(i, x)
    model.summary()

    model.compile(loss=params['loss'],
                  optimizer=Adam(params['adam-lr'], params['adam-beta_1']),
                  metrics=params['metrics'])
    return model


def discriminator_params():
    params = dict()

    params['alpha-l1'] = 0.2
    params['alpha-l2'] = 0.2
    params['alpha-l3'] = 0

    params['l1'] = 512
    params['l2'] = 256
    params['l3'] = 1

    params['activation'] = 'sigmoid'
    params['loss'] = 'binary_crossentropy'
    # def 0.001
    params['adam-lr'] = 0.0002
    # def 0.9
    params['adam-beta_1'] = 0.5
    params['metrics'] = ['accuracy']

    return params


def combined_model_params():
    params = dict()

    params['loss'] = 'binary_crossentropy'
    params['adam-lr'] = 0.0002
    params['adam-beta_1'] = 0.5

    return params


def create_combined_model(generator, discriminator, latent_dim, params):
    # create an input to represent noise sample from latent space
    z = Input(shape=(latent_dim,))
    # Pass noise through generator to get an image
    img = generator(z)

    # make sure only the generator is trained
    discriminator.trainable = False

    # The true output is fake, but we label them real!
    fake_pred = discriminator(img)

    # Create the combined model object
    combined_model = Model(z, fake_pred)

    # Compile the combined model
    combined_model.compile(loss=params['loss'],
                           optimizer=Adam(params['adam-lr'], params['adam-beta_1']))
    combined_model.summary()

    return combined_model


# def sample_images(epoch, latent_dim, imgs, H, W):
def sample_images(epoch, latent_dim, generator, H, W):
    rows, cols = 5, 5
    noise = np.random.randn(rows*cols, latent_dim)
    imgs = generator.predict(noise)

    # Rescale images 0 - 1
    imgs = 0.5 * imgs + 0.5

    fig, axs = plt.subplots(rows, cols)
    idx = 0
    for i in range(rows):
        for j in range(cols):
            axs[i, j].imshow(imgs[idx].reshape(H, W), cmap='gray')
            axs[i, j].axis('off')
            idx += 1
    fig_name = os.path.join(OUT_DIR, "fig" + str(epoch))
    fig.savefig(fig_name)
    plt.close()


def train_the_gan(batch_size, epochs, latent_dim, sample_period, x_train, generator, discriminator, combined_model, H, W):
    # every sample_period steps generate and same some data
    # Create batch labels to use when calling train_on_batch
    ones = np.ones(batch_size)
    zeros = np.zeros(batch_size)

    # Store the losses
    d_losses = []
    g_losses = []

    # Main training loop
    for epoch in range(epochs):
        #################################
        ### Train Discriminator
        #################################

        # Select a random batch of images
        idx = np.random.randint(0, x_train.shape[0], batch_size)
        real_imgs = x_train[idx]

        # Generate fake imatges
        noise = np.random.randn(batch_size, latent_dim)
        fake_imgs = generator.predict(noise)

        # Train the discriminator
        # both loss and accuracy are returned
        d_loss_real, d_acc_real = discriminator.train_on_batch(real_imgs, ones)
        d_loss_fake, d_acc_fake = discriminator.train_on_batch(fake_imgs, zeros)
        d_loss = 0.5*(d_loss_real + d_loss_fake)
        d_acc = 0.5*(d_acc_real + d_acc_fake)

        #################################
        ### Train Generator
        #################################
        noise = np.random.randn(batch_size, latent_dim)
        g_loss = combined_model.train_on_batch(noise, ones)

        # Save the losses
        d_losses.append(d_loss)
        g_losses.append(g_loss)

        if epoch % 100 == 0:
            print(f"epoch: {epoch + 1}/{epochs}, d_loss: {d_loss:.2f}, \
                  d_acc: {d_acc:.2f}, g_loss: {g_loss:.2f}")

        if epoch % sample_period == 0:
            sample_images(epoch, latent_dim, generator, H, W)


def main():
    # load the data
    D, N, H, W, (x_train, y_train), (x_test, y_test) = load_mnist_dataset()

    # generator
    latent_dim, param_generator = generator_params()
    gen = build_generator(latent_dim=latent_dim, params=param_generator, input_dimension=D)

    # discriminator
    params_discriminator = discriminator_params()
    dis = build_discriminator(img_size=D, params=params_discriminator)

    params_combined_model = combined_model_params()
    combined_model = create_combined_model(generator=gen,
                                           discriminator=dis,
                                           latent_dim=latent_dim,
                                           params=params_combined_model)
    train_the_gan(batch_size=32,
                  epochs=30000,
                  latent_dim=latent_dim,
                  sample_period=200,
                  x_train=x_train,
                  generator=gen,
                  discriminator=dis,
                  combined_model=combined_model,
                  H=H,
                  W=W)




if __name__ == '__main__':
    print(tf.__version__)
    main()
