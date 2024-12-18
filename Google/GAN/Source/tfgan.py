# -*- coding: utf-8 -*-
"""Sandbox_02.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DmKXAumE4oIndOz4wRyMH2S91WZcXwEX
"""



# Commented out IPython magic to ensure Python compatibility.
# !pip install tensorflow-gan
import tensorflow as tf
# import tensorflow.compat.v1 as tf
import tensorflow_gan as tfgan
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import os

# %matplotlib inline
# tf.version.VERSION
# tf.logging.set_verbosity(tf.logging.ERROR)

class InputHelper:

    @staticmethod
    def _preprocess(element):
        """
        preprocess mnist images, map value range from [0, 255] to [-1, 1]
        """
        images = (tf.cast(element['image'], tf.float32) - 127.5) / 127.5
        return images


    @staticmethod
    def input_fn(mode, params={'batch_size':100, 'noise_dims':64}):
        """
        Outputs for Each Mode
        1. Training Mode (tf.estimator.ModeKeys.TRAIN):
        - The function returns a zipped dataset of noise samples and preprocessed MNIST images.
        - The images are shuffled.
        - Output: (noise_batch, image_batch) where noise_batch has shape [batch_size, noise_dims] and image_batch has shape [batch_size, 28, 28, 1].
        2. Prediction Mode (tf.estimator.ModeKeys.PREDICT):
        - The function returns only the noise dataset.
        - Output: noise_batch where noise_batch has shape [batch_size, noise_dims].
        3. Evaluation Mode (tf.estimator.ModeKeys.EVAL):
        - The function returns a zipped dataset of noise samples and preprocessed MNIST images.
        - The images are not shuffled.
        - Output: (noise_batch, image_batch) where noise_batch has shape [batch_size, noise_dims] and image_batch has shape [batch_size, 28, 28, 1].
        """
        assert 'batch_size' in params
        assert 'noise_dims' in params
        batch_size = params['batch_size']
        noise_dims = params['noise_dims']
        split = 'train' if mode == tf.estimator.ModeKeys.TRAIN else 'test'
        shuffle = (mode == tf.estimator.ModeKeys.TRAIN)
        just_noise = (mode == tf.estimator.ModeKeys.PREDICT)
        noise_ds = (tf.data.Dataset.from_tensors(0).repeat()
                    .map(lambda _: tf.random.normal([batch_size, noise_dims])))
        if just_noise:
            return noise_ds
        images_ds = (tfds.load('mnist:3.*.*', split=split)
                    .map(InputHelper._preprocess)
                    .cache()
                    .repeat())
        if shuffle:
            images_ds = images_ds.shuffle(buffer_size=10000, reshuffle_each_iteration=True)
        images_ds = (images_ds.batch(batch_size, drop_remainder=True).prefetch(tf.data.experimental.AUTOTUNE))
        return tf.data.Dataset.zip((noise_ds, images_ds))

    @staticmethod
    def test_input_fn():
        ret = InputHelper.input_fn(tf.estimator.ModeKeys.TRAIN)
        element_spec = ret.element_spec
        noise_shape = element_spec[0].shape
        image_shape = element_spec[1].shape
        print("Noise batch dimensionality:", noise_shape)
        print("Image batch dimensionality:", image_shape)


InputHelper.test_input_fn()

import tensorflow_datasets as tfds

# This line creates a new TensorFlow graph as the default graph for all operations within the with block. This is useful to isolate operations and variables from other graphs.
with tf.Graph().as_default():
    # The method is called with parameters to operate in training mode (tf.estimator.ModeKeys.TRAIN), with a batch size of 100 and noise dimensions of 64.
    # This method returns a tf.data.Dataset object that produces pairs of noise vectors and MNIST images.
    ds = InputHelper.input_fn(tf.estimator.ModeKeys.TRAIN, {'batch_size':100, 'noise_dims':64})
    # tfds.as_numpy(ds) converts the tf.data.Dataset to an iterator that yields numpy arrays.
    # next(iter(...)) gets the first batch from this iterator.
    # he [1] at the end extracts the images batch from the pair (noise_batch, image_batch). noise_batch is at index 0 and image_batch is at index 1.
    numpy_imgs = next(iter(tfds.as_numpy(ds)))[1]
    numpy_rand = next(iter(tfds.as_numpy(ds)))[0]
    print("numpy_imgs.shape:{} numpy_rand.shape:{}".format(numpy_imgs.shape, numpy_rand.shape))
img_grid = tfgan.eval.python_image_grid(numpy_imgs, grid_shape=(10, 10))
plt.axis('off')
plt.imshow(np.squeeze(img_grid))
plt.show()
print(numpy_rand)

class NNHelper:

    leaky_relu = lambda x: tf.nn.leaky_relu(x, alpha=0.01)

    @staticmethod
    def dense(inputs, units, l2_weight):
        return tf.layers.dense(inputs,
                                units,
                                None,
                                kernel_initializer=tf.keras.initializers.glorot_uniform,
                                kernel_regularizer=tf.keras.regularizers.l2(l=l2_weight),
                                bias_regularizer=tf.keras.regularizers.l2(l=l2_weight))


    @staticmethod
    def batch_norm(inputs, is_training):
        return tf.layers.batch_normalization(inputs,
                                            momentum=0.999,
                                            epsilon=0.001,
                                            training=is_training)

    @staticmethod
    def deconv2d(inputs, filters, kernel_size, stride, l2_weight):
        return tf.layers.conv2d_transpose(inputs,
                                        filters,
                                        [kernel_size, kernel_size],
                                        strides=[stride, stride],
                                        activation=tf.nn.relu,
                                        padding='same',
                                        kernel_initializer=tf.keras.initializers.glorot_uniform,
                                        kernel_regularizer=tf.keras.regularizers.l2(l=l2_weight),
                                        bias_regularizer=tf.keras.regularizers.l2(l=l2_weight))

    @staticmethod
    def conv2d(inputs, filters, kernel_size, stride, l2_weight):
        return tf.layers.conv2d(inputs,
                                filters,
                                [kernel_size, kernel_size],
                                [stride, stride],
                                activation=None,
                                padding='same',
                                kernel_initializer=tf.keras.initializers.glorot_uniform,
                                kernel_regularizer=tf.keras.regularizers.l2(l=l2_weight),
                                bias_regularizer=tf.keras.regularizers.l2(l=l2_weight))


def unconditional_generator(noise, mode, weight_decay=2.5e-5):
    """
    Generator to produce unconditional MNIST images.
    """
    is_training = (mode == tf.estimator.ModeKeys.TRAIN)
    # L1
    net = NNHelper.dense(noise, 1024, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.relu(net)
    # L2
    net= NNHelper.dense(net, 7*7*256, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.relu(net)
    # L3
    net = tf.reshape(net, [-1, 7, 7, 256])
    net = NNHelper.deconv2d(net, 64, 4, 2, weight_decay)
    net = NNHelper.deconv2d(net, 64, 4, 2, weight_decay)
    net = NNHelper.conv2d(net, 1, 4, 1, 0.0)
    net = tf.tanh(net)

    return net

def unconditional_generator_v2(noise, mode, weight_decay=2.5e-5):
    """
    Generator to produce unconditional MNIST images.
    """
    is_training = (mode == tf.estimator.ModeKeys.TRAIN)

    # L1
    net = NNHelper.dense(noise, 1024, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.relu(net)
    # L2
    net= NNHelper.dense(net, 7*7*256, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.relu(net)
    # L3
    net = tf.reshape(net, [-1, 7, 7, 256])
    net = NNHelper.deconv2d(net, 64, 4, 2, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.relu(net)
    # L4
    net = NNHelper.deconv2d(net, 32, 4, 2, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.relu(net)

    # Out
    net = NNHelper.conv2d(net, 1, 4, 1, 0.0)
    net = tf.tanh(net)

    return net

def unconditional_generator_v3(noise, mode, weight_decay=2.5e-5):
    """
    Generator to produce unconditional MNIST images.
    """
    is_training = (mode == tf.estimator.ModeKeys.TRAIN)

    # L1
    net = NNHelper.dense(noise, 1024, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = tf.nn.leaky_relu(net)
    #net = tf.nn.relu(net)
    # L2
    net= NNHelper.dense(net, 7*7*256, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    #net = tf.nn.relu(net)
    net = tf.nn.leaky_relu(net)
    # L3
    net = tf.reshape(net, [-1, 7, 7, 256])
    net = NNHelper.deconv2d(net, 64, 4, 2, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    #net = tf.nn.relu(net)
    net = tf.nn.leaky_relu(net)
    # L4
    net = NNHelper.deconv2d(net, 32, 4, 2, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    #net = tf.nn.relu(net)
    net = tf.nn.leaky_relu(net)

    # Out
    net = NNHelper.conv2d(net, 1, 4, 1, 0.0)
    net = tf.tanh(net)

    return net




def unconditional_discriminator(img, unused_conditioning, mode, weight_decay=2.5e-5):
    """
    Discriminator to classify MNIST images.
    """
    del unused_conditioning
    is_training = (mode == tf.estimator.ModeKeys.TRAIN)

    net = NNHelper.conv2d(img, 64, 4, 2, weight_decay)
    net = NNHelper.leaky_relu(net)

    net = NNHelper.conv2d(net, 128, 4, 2, weight_decay)
    net = NNHelper.leaky_relu(net)

    net = tf.layers.flatten(net)
    net = NNHelper.dense(net, 1024, weight_decay)
    net = NNHelper.batch_norm(net, is_training)
    net = NNHelper.leaky_relu(net)

    net = NNHelper.dense(net, 1, weight_decay)

    return net

from tensorflow_gan.examples.mnist import util as eval_util
import os

def get_eval_metric_ops_fn(gan_model):
    real_data_logits = tf.reduce_mean(gan_model.discriminator_real_outputs)
    gen_data_logits = tf.reduce_mean(gan_model.discriminator_gen_outputs)
    real_mnist_score = eval_util.mnist_score(gan_model.real_data)
    generated_mnist_score = eval_util.mnist_score(gan_model.generated_data)
    frechet_distance = eval_util.mnist_frechet_distance(
        gan_model.real_data, gan_model.generated_data)
    return {
        'real_data_logits': tf.metrics.mean(real_data_logits),
        'gen_data_logits': tf.metrics.mean(gen_data_logits),
        'real_mnist_score': tf.metrics.mean(real_mnist_score),
        'mnist_score': tf.metrics.mean(generated_mnist_score),
        'frechet_distance': tf.metrics.mean(frechet_distance),
    }

train_batch_size = 32
noise_dimensions = 64
generator_lr = 0.001
discriminator_lr = 0.0002

def gen_opt():
    gstep = tf.train.get_or_create_global_step()
    base_lr = generator_lr
    lr = tf.cond(gstep < 1000, lambda: base_lr, lambda: base_lr / 2.0)
    return tf.train.AdamOptimizer(lr, 0.5)

gan_estimator = tfgan.estimator.GANEstimator(
    generator_fn=unconditional_generator_v3,
    discriminator_fn=unconditional_discriminator,
    generator_loss_fn=tfgan.losses.wasserstein_generator_loss,
    discriminator_loss_fn=tfgan.losses.wasserstein_discriminator_loss,
    params={'batch_size': train_batch_size, 'noise_dims': noise_dimensions},
    generator_optimizer=gen_opt,
    discriminator_optimizer=tf.train.AdamOptimizer(discriminator_lr, 0.5),
    get_eval_metric_ops_fn=get_eval_metric_ops_fn
)

import time

tf.autograph.set_verbosity(0, False)

steps_per_eval = 500
max_train_steps = 5000
batches_for_eval_metrics = 100

# track metrics
steps = []
real_logits = []
fake_logits = []
real_mnist_scores = []
mnist_scores = []
frechet_distances = []

cur_step = 0
start_time = time.time()
while cur_step < max_train_steps:
    next_step = min(cur_step + steps_per_eval, max_train_steps)

    start = time.time()
    gan_estimator.train(InputHelper.input_fn, max_steps=next_step)
    steps_taken = next_step - cur_step
    time_taken = time.time() - start
    print('Time since start: %.2f min' % ((time.time() - start_time) / 60.0))
    print('Trained from step %i to %i in %.2f steps / sec' % (cur_step, next_step, steps_taken / time_taken))
    cur_step = next_step

    # calculate some metrics
    metrics = gan_estimator.evaluate(InputHelper.input_fn, steps=batches_for_eval_metrics)
    steps.append(cur_step)
    real_logits.append(metrics['real_data_logits'])
    fake_logits.append(metrics['gen_data_logits'])
    real_mnist_scores.append(metrics['real_mnist_score'])
    mnist_scores.append(metrics['mnist_score'])
    frechet_distances.append(metrics['frechet_distance'])
    print('Average discriminator output on Real: %.2f  Fake: %.2f' % (real_logits[-1], fake_logits[-1]))
    print('Inception Score: %.2f / %.2f  Frechet Distance: %.2f' % (mnist_scores[-1], real_mnist_scores[-1], frechet_distances[-1]))

    print('Time since start: %.2f min' % ((time.time() - start_time) / 60.0))
    print('Trained from step %i to %i in %.2f steps / sec' % (cur_step, next_step, steps_taken / time_taken))

    print('Average discriminator output on Real: %.2f  Fake: %.2f' % (real_logits[-1], fake_logits[-1]))
    print('Inception Score: %.2f / %.2f  Frechet Distance: %.2f' % (mnist_scores[-1], real_mnist_scores[-1], frechet_distances[-1]))

    # Vizualize some images.
    iterator = gan_estimator.predict(InputHelper.input_fn, hooks=[tf.train.StopAtStepHook(num_steps=21)])
    try:
        imgs = np.array([next(iterator) for _ in range(20)])
    except StopIteration:
        pass

    tiled = tfgan.eval.python_image_grid(imgs, grid_shape=(2, 10))
    plt.axis('off')
    plt.imshow(np.squeeze(tiled))
    plt.show()


# Plot the metrics vs step.
plt.title('MNIST Frechet distance per step')
plt.plot(steps, frechet_distances)
plt.figure()
plt.title('MNIST Score per step')
plt.plot(steps, mnist_scores)
plt.plot(steps, real_mnist_scores)
plt.show()