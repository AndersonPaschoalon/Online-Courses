import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, GlobalMaxPooling2D
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from Utils import Utils

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
    loss_function = 'sparse_categorical_crossentropy'
    optimizer_func = 'adam'
    # model build
    i = Input(shape=input_shape)
    x = Conv2D(cl1, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(i)
    x = Conv2D(cl2, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(x)
    x = Conv2D(cl3, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(x)
    x = Flatten()(x)
    x = Dropout(0.2)(x)
    x = Dense(dl1, activation=actv_function_dense)(x)
    x = Dropout(0.2)(x)
    x = Dense(dl2, activation=actv_function_out)(x)
    model = Model(i, x)
    # compile
    model.compile(optimizer=optimizer_func,
                  loss=loss_function,
                  metrics=['accuracy'])
    return model

def train_the_model(model, x_train, y_train, x_test, y_test, n_epochs):
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)
    return r

def plot_loss_and_accurary_per_iteration(r, out_dir=""):
    out_dir += "\\"
    # plot loss per iteration
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.savefig(out_dir + "loss_per_iteration")
    # plot accuracy per iteration
    plt.clf()
    plt.plot(r.history['accuracy'], label='acc')
    plt.plot(r.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.savefig(out_dir + "accuracy_per_iteration")

def plot_confusion_matrix(model, x_test, y_test, out_dir):
    out_dir += "\\"
    p_test = model.predict(x_test).argmax(axis=1)
    cm = confusion_matrix(y_test, p_test)
    Utils.plot_confusion_matrix(cm, list(range(10)), out_file_name= out_dir + "CnnFashionMnist_ConfusionMatrix")


def main():
    n_epochs = 2
    out_dir = "32"
    (x_train, y_train), (x_test, y_test), K = load_fashion_mnist(out_dir)
    model = build_the_model(input_shape=x_train[0].shape, number_of_classes=K)
    r = train_the_model(model, x_train, y_train, x_test, y_test, n_epochs=n_epochs)
    plot_loss_and_accurary_per_iteration(r, out_dir=out_dir)
    plot_confusion_matrix(model, x_test, y_test, out_dir)

if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()

