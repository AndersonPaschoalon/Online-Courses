import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, GlobalMaxPooling2D
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt


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
def load_fashion_mnist(out_dir=""):
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
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    # calc number of classes
    K = len(set(y_train))
    print("number of classes of FahionMNIST:", K)
    return (x_train, y_train), (x_test, y_test), K

# build the moel using function API
def build_the_model(input_shape, number_of_classes):
    # model hyperparameters
    kernel_size = (3, 3)
    cl1 = 32
    cl2 = 64
    cl3 = 128
    dl1 = 512
    dl2 = number_of_classes
    strides = 2
    actv_function_conv = 'relu'
    actv_function_dense = 'relu'
    actv_function_out = 'softmax'
    optimizer_func = 'adam'

    # model build
    i = Input(shape=input_shape)
    x = Conv2D(cl1, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(i)
    x = Conv2D(cl2, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(x)
    x = Conv2D(cl3, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(x)
    x = Flatten()(x)
    x = Dropout(0.2)(x)
    x = Dense(dl1, activation=actv_function_dense)
    x = Dropout(0.2)(x)
    x = Dense(dl2, activation=actv_function_out)
    model = Model(i, x)

    # compile
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def train_the_model(model, x_train, y_train, x_test, y_test, n_epochs):
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)
    return r



def main():
    n_epochs=2
    (x_train, y_train), (x_test, y_test), K = load_fashion_mnist("32")
    model = build_the_model(input_shape=x_train[0].shape, number_of_classes=K)
    r = train_the_model(model, x_train, y_train, x_test, y_test, n_epochs=n_epochs )

if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()

