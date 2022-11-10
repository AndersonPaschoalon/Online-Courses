# https://deeplearningcourses.com/c/advanced-computer-vision
# https://www.udemy.com/advanced-computer-vision

from __future__ import print_function, division
from builtins import range, input

import traceback
import sys
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future

from keras.models import Model, Sequential
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

from _69_StyleTransfer import VGG16_AvgPool, unpreprocess, scale_img, helper_keras_load_image
from Utils import Utils

# from skimage.transform import resize
from scipy.optimize import fmin_l_bfgs_b
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import keras.backend as K

from datetime import datetime
import os

import tensorflow as tf

if tf.__version__.startswith('2'):
    tf.compat.v1.disable_eager_execution()

GPU_REQUIRED_TF_VERSION = "2.6"


def gram_matrix(img):
    # input is (H, W, C) (C = # feature maps)
    # we first need to convert it to (C, H*W)
    X = K.batch_flatten(K.permute_dimensions(img, (2, 0, 1)))

    # now, calculate the gram matrix
    # gram = XX^T / N
    # the constant is not important since we'll be weighting these
    G = K.dot(X, K.transpose(X)) / img.get_shape().num_elements()
    return G


def style_loss(y, t):
    return K.mean(K.square(gram_matrix(y) - gram_matrix(t)))


def minimize(fn, epochs, batch_shape, out_dir, model_name):
    """
    Lets generarize this and put into a function.
    """
    t0 = datetime.now()
    losses = []
    x = np.random.randn(np.prod(batch_shape))
    for i in range(epochs):
        x, l, _ = fmin_l_bfgs_b(func=fn,
                              x0=x,
                              maxfun=20)
        x = np.clip(x, -127, 127)
        print("item=%s, loss=%s" % (i,  l))
        losses.append(l)
    print("duration:", datetime.now() - t0)

    out_dir = out_dir + "\\"
    plt.clf()
    plt.plot(losses)
    plt.savefig(out_dir + "losses_" + model_name + ".jpg")

    newimg = x.reshape(*batch_shape)
    final_img = unpreprocess(newimg)
    return final_img[0]


def run_style_transfer_pt2(path, out_dir):
    try:
        out_dir = out_dir + "\\"
        image_name = Utils.file_name(path)

        # load the data
        img = helper_keras_load_image(path)

        # convert image to array and preprocess for vgg
        # x = image.img_to_array(img)
        x = tf.keras.utils.img_to_array(img)

        # look at the image
        plt.clf()
        plt.imshow(x)
        plt.savefig(out_dir + "vgg_preprocess_" + image_name + ".jpg")

        # make it (1, H, W, C)
        x = np.expand_dims(x, axis=0)

        # preprocess into VGG expected format
        x = preprocess_input(x)

        # Well use this through the rest of the script
        batch_shape = x.shape
        shape = x.shape[1:]

        # let's take the first convolution at each block of convolutions
        # to be our target outputs
        # remember that you can print out the model summary if you want
        vgg = VGG16_AvgPool(shape)
        vgg.summary()

        # Note: need to select output at index 1, since outputs at
        # index 0 correspond to the original vgg with maxpool
        symbolic_conv_outputs = [
        layer.get_output_at(1) for layer in vgg.layers \
            if layer.name.endswith('conv1')
        ]

        # pick the earlier layers for
        # a more "localized" representation
        # this is opposed to the content model
        # where the later layers represent a more "global" structure
        # symbolic_conv_outputs = symbolic_conv_outputs[:2]

        # make a big model that outputs multiple layers' outputs
        multi_output_model = Model(vgg.input, symbolic_conv_outputs)

        # calculate the targets that are output at each layer
        style_layers_outputs = [K.variable(y) for y in multi_output_model.predict(x)]

        # calculate the total style loss
        loss = 0
        for symbolic, actual in zip(symbolic_conv_outputs, style_layers_outputs):
            # gram_matrix() expects a (H, W, C) as input
            loss += style_loss(symbolic[0], actual[0])

        grads = K.gradients(loss, multi_output_model.input)

        # just like theano.function
        get_loss_and_grads = K.function(
        inputs=[multi_output_model.input],
            outputs=[loss] + grads
        )

        def get_loss_and_grads_wrapper(x_vec):
            l, g = get_loss_and_grads([x_vec.reshape(*batch_shape)])
            return l.astype(np.float64), g.flatten().astype(np.float64)

        final_img = minimize(get_loss_and_grads_wrapper, 10, batch_shape, out_dir, image_name)

        # save the image
        plt.clf()
        plt.imshow(scale_img(final_img))
        plt.savefig(out_dir + "styled_image_" + image_name + ".jpg")
    except:
        print("***EXCEPTION***")
        traceback.print_exc()


if __name__ == '__main__':
    print("* For running on CPU, it is required Python 3.9 and TensorFlow 2.10.0")
    print("* For running on GPU, it is required Python 3.6 and TensorFlow 2.6")
    print("")
    print("TensorFlow version:", tf.__version__)
    print("Python Version: ", sys.version)
    print("Python Version Info: ", sys.version_info)

    out_dir = "70"
    run_style_transfer_pt2("70/starry_night.jpg", out_dir)
    run_style_transfer_pt2("70/fantasy_city.png", out_dir)
    run_style_transfer_pt2("70/fantasy_city2.png", out_dir)
    run_style_transfer_pt2("70/fantasy_city3.png", out_dir)
    run_style_transfer_pt2("70/fantasy_city4.png", out_dir)
    run_style_transfer_pt2("70/fantasy_landscape1.png", out_dir)
    run_style_transfer_pt2("70/fantasy_landscape2.png", out_dir)
    run_style_transfer_pt2("70/fantasy_landscape3.png", out_dir)
    run_style_transfer_pt2("70/skyrim_landscape1.png", out_dir)
    run_style_transfer_pt2("70/skyrim_landscape2.png", out_dir)
    run_style_transfer_pt2("70/skyrim_landscape3.png", out_dir)
    run_style_transfer_pt2("70/fantasy_landscape3.png", out_dir)