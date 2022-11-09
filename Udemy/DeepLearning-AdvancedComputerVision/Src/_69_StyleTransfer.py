# https://deeplearningcourses.com/c/advanced-computer-vision
# https://www.udemy.com/advanced-computer-vision

from __future__ import print_function, division

import sys
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future

# In this script, we will focus on generating the content
# E.g. given an image, can we recreate the same image

from keras.layers import Input, Lambda, Dense, Flatten
from keras.layers import AveragePooling2D, MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.models import Model, Sequential
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image

import keras.backend as K
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import fmin_l_bfgs_b
from datetime import datetime
import os

import tensorflow as tf
if tf.__version__.startswith('2'):
    tf.compat.v1.disable_eager_execution()

GPU_REQUIRED_TF_VERSION = "2.6"

def VGG16_AvgPool(shape):
    """
    The purpose of this function is to recreate a VGG neural network, but that uses average pooling instead of max
    pooling. In this case was observed that average pooling performs better than maxpooling. The reason might
    be that max pooling discards data, while average pooling keeps all the data.
    :param shape:
    :return:
    """
    vgg = VGG16(input_shape=shape, weights='imagenet', include_top=False)
    # new_model = Sequential()
    # for layer in vgg.layers:
    #   if layer.__class__ == MaxPooling2D:
    #     # replace it with average pooling
    #     new_model.add(AveragePooling2D())
    #   else:
    #     new_model.add(layer)
    i = vgg.input
    x = i
    for layer in vgg.layers:
        if layer.__class__ == MaxPooling2D:
            # replace it with average pooling
            x = AveragePooling2D()(x)
        else:
            x = layer(x)

    return Model(i, x)


def VGG16_AvgPool_CutOff(shape, num_convs):
    """
    The idea is that we might choose wich layer performs better the task, so we can pick any of the 13 layers as the
    output.
    :param shape:
    :param num_convs:
    :return:
    """
    if num_convs < 1 or num_convs > 13:
        print("num_convs must be in the range [1, 13]")
        return None

    model = VGG16_AvgPool(shape)
    n = 0
    output = None
    for layer in model.layers:
        if layer.__class__ == Conv2D:
            n += 1
        if n >= num_convs:
            output = layer.output
            break

    return Model(model.input, output)


def unpreprocess(img):
    """
    VGG expects a different format of file as matplotlib for the images. It basically reverse the preprocess required
    by VGG, so we can visualize the images on matplotlib as usual.
    :param img:
    :return:
    """
    img[..., 0] += 103.939
    img[..., 1] += 116.779
    img[..., 2] += 126.68
    img = img[..., ::-1]
    return img


def scale_img(x):
    """
    Scale the pixesl between 0 and 1.
    :param x:
    :return:
    """
    x = x - x.min()
    x = x / x.max()
    return x

def get_loss_and_grads_wrapper(x_vec):
    # scipy's minimizer allows us to pass back
    # function value f(x) and its gradient f'(x)
    # simultaneously, rather than using the fprime arg
    #
    # we cannot use get_loss_and_grads() directly
    # input to minimizer func must be a 1-D array
    # input to get_loss_and_grads must be [batch_of_images]
    #
    # gradient must also be a 1-D array
    # and both loss and gradient must be np.float64
    # will get an error otherwise

    l, g = get_loss_and_grads([x_vec.reshape(*batch_shape)])
    return l.astype(np.float64), g.flatten().astype(np.float64)

def run_style_transfer_pt1(out_dir, image_file, nn_cutoff):
    # print run information
    print("Running style transfer -> out_dir:", out_dir, ", image_file:", image_file, ", nn_cutoff:", nn_cutoff)

    # parse vars
    out_dir = out_dir + "\\"
    path = os.path.join(out_dir, image_file)
    image_name = os.path.basename(os.path.splitext(image_file)[0])

    # load image
    img = None
    tf_version = str(tf.__version__)
    if tf_version.startswith(GPU_REQUIRED_TF_VERSION):
        print("Tensorflow version for GPU usage matches... running on GPU mode...")
        img = image.load_img(path)
    else:
        print("Running on CPU mode")
        img = tf.keras.utils.load_img(path)

    # convert the image to array and process for vgg
    # x = image.img_to_array(img)
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # we'll use this through the rest of the script
    batch_shape = x.shape
    shape = x.shape[1:]

    # make a content model
    # try different cutoffs to see the images that result
    # nn_cutoff = 11
    content_model = VGG16_AvgPool_CutOff(shape, nn_cutoff)

    # make the target
    target = K.variable(content_model.predict(x))

    # try to match the image

    # define our loss in keras
    #loss = K.mean(K.square(target=content_model.output))
    loss = K.mean(K.square(target - content_model.output))

    # gradients which are needed by the optimizer
    grads = K.gradients(loss, content_model.input)
    # grads = K.gradients(loss, content_model.trainable_variables)

    # just like theano funcion
    get_loss_and_grads = K.function(inputs=[content_model.input],
                                    outputs=[loss] + grads)

    # generate the images
    t0 = datetime.now()
    losses = []
    x = np.random.randn(np.prod(batch_shape))
    for i in range(10):
        x, l, _ = fmin_l_bfgs_b(func=get_loss_and_grads_wrapper,
                                x0=x,
                                # bounds = [[-127, 127]]*len(x.flatten()),
                                maxfun=20)
        x = np.clip(x, -127, 127)
        # print("min:", x.min(), "max:", x.max())
        print("iter=%s, loss=%s" % (i, l))
        losses.append(l)

    print("duration:", datetime.now() - t0)

    plt.clf()
    plt.plot(losses)
    plt.savefig(out_dir + "losses.jpg")

    plt.clf()
    newimg = x.reshape(*batch_shape)
    final_img = unpreprocess(newimg)
    plt.imshow(scale_img(final_img[0]))
    plt.savefig(out_dir + "final_img" + "_" + image_name + "_" + str(nn_cutoff) + ".jpg")


"""
if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    # open an image
    out_dir = "69\\"
    # path = "69\\forest.jpg"
    #img_name = "gato"
    #path = "69\\gato.jpg"
    img_name = "elefante"
    path = "69\\elefante.jpg"
    img = image.load_img(path)
    # img = tf.keras.utils.load_img(path)

    # convert the image to array and process for vgg
    # x = image.img_to_array(img)
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # we'll use this through the rest of the script
    batch_shape = x.shape
    shape = x.shape[1:]

    # >>>>>>>

    # make a content model
    # try different cutoffs to see the images that result
    nn_cutoff = 11
    content_model = VGG16_AvgPool_CutOff(shape, nn_cutoff)

    # make the target
    target = K.variable(content_model.predict(x))

    # try to match the image

    # define our loss in keras
    #loss = K.mean(K.square(target=content_model.output))
    loss = K.mean(K.square(target - content_model.output))

    # gradients which are needed by the optimizer
    grads = K.gradients(loss, content_model.input)
    # grads = K.gradients(loss, content_model.trainable_variables)

    # just like theano funcion
    get_loss_and_grads = K.function(inputs=[content_model.input],
                                    outputs=[loss] + grads)

    # generate the images
    t0 = datetime.now()
    losses = []
    x = np.random.randn(np.prod(batch_shape))
    for i in range(10):
        x, l, _ = fmin_l_bfgs_b(func=get_loss_and_grads_wrapper,
                                x0=x,
                                # bounds = [[-127, 127]]*len(x.flatten()),
                                maxfun=20)
        x = np.clip(x, -127, 127)
        # print("min:", x.min(), "max:", x.max())
        print("iter=%s, loss=%s" % (i, l))
        losses.append(l)

    print("duration:", datetime.now() - t0)

    plt.clf()
    plt.plot(losses)
    plt.savefig(out_dir + "losses.jpg")

    plt.clf()
    newimg = x.reshape(*batch_shape)
    final_img = unpreprocess(newimg)
    plt.imshow(scale_img(final_img[0]))
    plt.savefig(out_dir + "final_img" + "_" + img_name + "_" + str(nn_cutoff) + ".jpg")

"""

if __name__ == '__main__':
    print("* For running on CPU, it is required Python 3.9 and TensorFlow 2.10.0")
    print("* For running on GPU, it is required Python 3.6 and TensorFlow 2.6")
    print("")
    print("TensorFlow version:", tf.__version__)
    print("Python Version: ", sys.version)
    print("Python Version Info: ", sys.version_info)
    # open an image

    print("*ELEFANTE*")
    run_style_transfer_pt1(out_dir="69",
                           image_file="elefante.jpg",
                           nn_cutoff=11)
    run_style_transfer_pt1(out_dir="69",
                           image_file="elefante.jpg",
                           nn_cutoff=13)
    run_style_transfer_pt1(out_dir="69",
                           image_file="elefante.jpg",
                           nn_cutoff=5)

    print("*GATO*")
    run_style_transfer_pt1(out_dir="69",
                           image_file="gato.jpg",
                           nn_cutoff=11)
    run_style_transfer_pt1(out_dir="69",
                           image_file="gato.jpg",
                           nn_cutoff=13)
    run_style_transfer_pt1(out_dir="69",
                           image_file="gato.jpg",
                           nn_cutoff=5)












