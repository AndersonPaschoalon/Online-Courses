# https://deeplearningcourses.com/c/advanced-computer-vision
# https://www.udemy.com/advanced-computer-vision

from __future__ import print_function, division
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future

# In this script, we will focus on generating an image
# that attempts to match the content of one input image
# and the style of another input image.
#
# We accomplish this by balancing the content loss
# and style loss simultaneously.

from keras.layers import Input, Lambda, Dense, Flatten
from keras.layers import AveragePooling2D, MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.models import Model, Sequential
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from skimage.transform import resize

import tensorflow as tf
import traceback
import sys
from builtins import range, input
from datetime import datetime
import os
import keras.backend as K
import numpy as np
import matplotlib.pyplot as plt

from _69_StyleTransfer import VGG16_AvgPool, VGG16_AvgPool_CutOff,  unpreprocess, scale_img, helper_keras_load_image
from _70_StyleTransfer_pt2 import  gram_matrix, style_loss, minimize
from Utils import Utils
from scipy.optimize import fmin_l_bfgs_b

# load the content image
def load_img_and_preprocess(path, shape=None):
    img = image.load_img(path, target_size=shape)

    # convert image to array and preprocess for vgg
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    return x


def run_style_transfer_pt3(path_image, path_style, out_dir, n_epochs):
    out_dir = out_dir + "\\"
    image_name = Utils.file_name(path_image)
    style_name = Utils.file_name(path_style)

    # load image
    content_img = load_img_and_preprocess(path_image,)

    # resize the style image
    # since we don't care too much about warping it
    h, w = content_img.shape[1:3]
    style_img = load_img_and_preprocess(path_style, (h, w))

    # we'll use this throughout the rest of the script
    batch_shape = content_img.shape
    shape = content_img.shape[1:]

    # we want to make only 1 VGG here
    # as you'll see later, the final model needs
    # to have a common input
    vgg = VGG16_AvgPool(shape)
    vgg.summary()

    # create the content model
    # we only want 1 output
    # remember you can call vgg.summary() to see a list of layers
    # 1,2,4,5,7-9,11-13,15-17
    content_model = Model(vgg.input, vgg.layers[13].get_output_at(0))
    content_target = K.variable(content_model.predict(content_img))

    # style

    # create the style model
    # we want multiple outputs
    # we will take the same approach as in style_transfer2.py
    symbolic_conv_outputs = [
        layer.get_output_at(1) for layer in vgg.layers \
        if layer.name.endswith('conv1')
    ]

    # make a big model that outputs multiple layers' outputs
    style_model = Model(vgg.input, symbolic_conv_outputs)

    # calculate the targets that are output at each layer
    style_layers_outputs = [K.variable(y) for y in style_model.predict(style_img)]

    # we will assume the weight of the content loss is 1
    # and only weight the style losses
    style_weights = [0.2, 0.4, 0.3, 0.5, 0.2]

    # create the total loss which is the sum of content + style loss
    loss = K.mean(K.square(content_model.output - content_target))

    for w, symbolic, actual in zip(style_weights, symbolic_conv_outputs, style_layers_outputs):
        # gram_matrix() expects a (H, W, C) as input
        loss += w * style_loss(symbolic[0], actual[0])

    # once again, create the gradients and loss + grads function
    # note: it doesn't matter which model's input you use
    # they are both pointing to the same keras Input layer in memory
    grads = K.gradients(loss, vgg.input)

    # just like theano.function
    get_loss_and_grads = K.function(
        inputs=[vgg.input],
        outputs=[loss] + grads
    )

    def get_loss_and_grads_wrapper(x_vec):
        l, g = get_loss_and_grads([x_vec.reshape(*batch_shape)])
        return l.astype(np.float64), g.flatten().astype(np.float64)

    final_image_name = image_name + "_" + style_name
    final_img = minimize(get_loss_and_grads_wrapper, n_epochs, batch_shape, out_dir, final_image_name)

    plt.clf()
    plt.imshow(scale_img(final_img))
    final_image_path = out_dir + "styled_image_" + final_image_name + ".jpg"
    plt.savefig(final_image_path)


if __name__ == '__main__':
    print("* For running on CPU, it is required Python 3.9 and TensorFlow 2.10.0")
    print("* For running on GPU, it is required Python 3.6 and TensorFlow 2.6")
    print("")
    print("TensorFlow version:", tf.__version__)
    print("Python Version: ", sys.version)
    print("Python Version Info: ", sys.version_info)
    out_dir = "71"

    path_image = "71/cidade1.png"
    path_style = "70/fantasy_city.png"
    run_style_transfer_pt3(path_image=path_image, path_style=path_style, out_dir=out_dir, n_epochs=10)