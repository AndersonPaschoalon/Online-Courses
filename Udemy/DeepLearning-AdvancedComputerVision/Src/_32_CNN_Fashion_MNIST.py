import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

MNIST_FASHION_LABELS = {
    "0": "TShirtTop",
    "1": "Trouser",
    "2": "Pullover",
    "3": "Dress",
    "4": "Coat",
    "5": "Sandal",
    "6": "Shirt",
    "7": "Sneaker",
    "8": "Bag",
    "9": "AnkleBoot"
 }


# Load the data
def load_fashion_mnist(out_dir = ""):
    # load data
    out_dir += "\\"
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
    print("x_train.shape:", x_train.shape)
    print("y_train.shape:", y_train.shape)
    print("x_test.shape:", x_test.shape)
    print("x_test.shape:", x_test.shape)
    # display some examples
    plt.clf()
    img_name = "mnist_test0_" + MNIST_FASHION_LABELS[str(y_test[0])]
    plt.imshow(x_test[0], cmap='gray')
    plt.savefig(out_dir + img_name)
    plt.clf()
    img_name = "mnist_train0_" + MNIST_FASHION_LABELS[str(y_train[0])]
    plt.imshow(x_train[0], cmap='gray')
    plt.savefig(out_dir + img_name)
    # regularization
    x_train, x_test = x_train/255.0, x_test/255.0
    # CNN requerem imagens 3d, mas os dados são 2d
    # convolution expects h x w x color
    x_tran = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    # calc number of classes
    K = len(set(y_train))
    print("number of classes of FahionMNIST:", K)
    return (x_train, y_train), (x_test, y_test), K


def main():
    print("todo")
    load_fashion_mnist("32")

if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()

