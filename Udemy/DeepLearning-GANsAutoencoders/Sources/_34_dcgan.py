import glob
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
from tensorflow.keras import layers
import tensorflow.compat.v1 as tf
import time
from IPython import display
from tqdm import tqdm

########################################################################################################################
# utils
########################################################################################################################


def center_images(images):
    # Pad the input images with zeros on all sides
    centered_images = tf.pad(images, [[0, 0], [18, 18], [18, 18]])
    # Repeat the images along the channel dimension to make them 3 channels
    centered_images = tf.repeat(tf.expand_dims(centered_images, axis=-1), 3, axis=-1)
    return centered_images


def generate_and_save_images(model, epoch, test_input, out_dir):
    # Notice `training` is set to False.
    # This is so all layers run in inference mode (batchnorm).
    predictions = model(test_input, training=False)
    fig = plt.figure(figsize=(4, 4))
    plt.clf()
    for i in range(predictions.shape[0]):
      plt.subplot(4, 4, i+1)
      plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
      plt.axis('off')
    plt.savefig(os.path.join(out_dir, 'image_at_epoch_{:04d}.png'.format(epoch)))



########################################################################################################################
# model
########################################################################################################################

def make_generator_model_google():
    model = tf.keras.Sequential()
    model.add(layers.Dense(7*7*256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((7, 7, 256)))
    assert model.output_shape == (None, 7, 7, 256)  # Note: None is the batch size

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    assert model.output_shape == (None, 7, 7, 128)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    assert model.output_shape == (None, 14, 14, 64)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    assert model.output_shape == (None, 28, 28, 1)

    return model


def make_discriminator_model():
    i = tf.keras.Input(shape=(28, 28, 1))
    # layer 01
    x = layers.Conv2D(61, (5, 5), strides=(2, 2), padding='same')(i)
    x = layers.LeakyReLU()(x)
    x = layers.Dropout(0.3)(x)
    # layer 02
    x = layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same')(x)
    x = layers.LeakyReLU()(x)
    x = layers.Dropout(0.3)(x)
    # Layer 03
    x = layers.Flatten()(x)
    x = layers.Dense(1)(x)
    # out
    model = tf.keras.Model(i, x)
    return model


def discriminator_loss(real_output, fake_output, cross_entropy):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output, cross_entropy):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


def test_generator_discriminator(g, d, out_dir):
    g.summary()
    print("G:", g.output_shape)
    d.summary()
    print("D:", d.output_shape)
    print("Test Generator")
    noise = tf.random.normal([10, 100])
    print("noise.shape=", noise.shape)
    generated_image = g(noise, training=False)
    print("generated_image.shape=", generated_image.shape)
    plt.clf()
    plt.imshow(generated_image[0, :, :, 0], cmap='gray')
    plt.savefig(os.path.join(out_dir, "gen_image_no_training"))
    print("Test Discriminator")
    generated_image = g(tf.random.normal([1, 100]), training=False)
    plt.imshow(generated_image[0, :, :, 0], cmap='gray')
    print("generated_image.shape:{}".format(generated_image[0, :, :, 0].shape))
    decision = d(generated_image)
    print("decision:", decision[0])


@tf.function
def train_step(images,
               batch_size,
               noise_dim,
               generator,
               generator_optimizer,
               discriminator,
               discriminator_optimizer,
               cross_entropy_func):
    # input noise
    noise = tf.random.normal([batch_size, noise_dim]) # batches of noise

    # generate fake images, and calc loss real vs fake
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        # create fake images
        gen_images = generator(noise, training=True)
        # discriminator results
        real_output = discriminator(images, training=True)
        fake_output = discriminator(gen_images, training=True)
        # calc loss
        gen_loss = generator_loss(fake_output, cross_entropy_func)
        disc_loss = discriminator_loss(real_output, fake_output, cross_entropy_func)

    # gradients
    grad_gen = gen_tape.gradient(gen_loss, generator.trainable_variables)
    grad_disc = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    # optimizer
    generator_optimizer.apply_gradients(zip(grad_gen, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(grad_disc, discriminator.trainable_variables))


def train(dataset,
          epochs,
          batch_size,
          noise_dim,
          generator,
          generator_optimizer,
          discriminator,
          discriminator_optimizer,
          cross_entropy_func,
          seed,
          checkpoint,
          checkpoint_prefix,
          out_dir):
    for epoch in tqdm(range(epochs)):
        start = time.time()
        # loop over all batches in dataset
        for image_batch in dataset:
            # print("image_batch.shape:", image_batch.shape)
            train_step(images=image_batch,
                       batch_size=batch_size,
                       noise_dim=noise_dim,
                       generator=generator,
                       generator_optimizer=generator_optimizer,
                       discriminator=discriminator,
                       discriminator_optimizer=discriminator_optimizer,
                       cross_entropy_func=cross_entropy_func)

        # save the model every 15 epochs
        if ((epoch + 1) % 5) == 0:
            print("-- ", (epoch + 1))
            # checkpoint.save(file_prefix=checkpoint_prefix)
            # Produce images for the GIF as you go
            display.clear_output(wait=True)
            generate_and_save_images(generator, epoch + 1, seed, out_dir)
        # print("Time for epoch {} is {} sec".format(epoch + 1, time.time() - start))

    # Generate image after the final epoch
    display.clear_output(wait=True)
    generate_and_save_images(generator, epochs, seed, out_dir)


def main():
    print("tf.__version__:", tf.__version__)

    (train_images, train_labels), (_, _) = tf.keras.datasets.mnist.load_data()
    BUFFER_SIZE = len(train_images)
    BATCH_SIZE = 256
    EPOCHS = 5000
    noise_dim = 100
    num_examples_to_generate = 16
    OUT_DIR = "Results/34/"
    # Otimizador: Adam lr=0.0002, beta1:0.5
    learning_rate = 2e-4
    beta1 = 0.5
    seed = tf.random.normal([num_examples_to_generate, noise_dim])
    print("BUFFER_SIZE:{}, BATCH_SIZE:{}, train_images.shape:{}".format(BUFFER_SIZE, BATCH_SIZE, train_images.shape))

    train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32')
    train_images = (train_images - 127.5) / 127.5  # Normalize the images to [-1, 1]

    g = make_generator_model_google()
    d = make_discriminator_model()
    test_generator_discriminator(g=g, d=d, out_dir=OUT_DIR)

    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
    generator_optimizer = tf.keras.optimizers.Adam(1e-4)
    discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
    g_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, beta_1=beta1)
    d_optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, beta_1=beta1)

    checkpoint_dir = './dcgan/training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
    print("checkpoint_dir:{}, checkpoint_prefix:{}".format(checkpoint_dir, checkpoint_prefix))
    checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                     discriminator_optimizer=discriminator_optimizer,
                                     generator=g,
                                     discriminator=d)

    train(dataset=train_dataset,
          epochs=EPOCHS,
          batch_size=BATCH_SIZE,
          noise_dim=noise_dim,
          generator=g,
          generator_optimizer=g_optimizer,
          discriminator=d,
          discriminator_optimizer=d_optimizer,
          cross_entropy_func=cross_entropy,
          seed=seed,
          checkpoint=checkpoint,
          checkpoint_prefix=checkpoint_prefix,
          out_dir=OUT_DIR)


main()