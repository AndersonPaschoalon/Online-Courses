import numpy as np
import sys
import matplotlib.pyplot

# using tf version 1
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from Utils import Utils

def error_rate(p, t):
    return np.mean(p != t)


def main():
    X, Y = Utils.get_normalized_data()
    print("todo")


if __name__ == '__main__':
    print(tf.__version__)
    main()
