import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, GlobalMaxPooling2D, BatchNormalization, MaxPooling2D
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from Utils import Utils
from random import randint

LABELS = """airplane 										
automobile 										
bird 										
cat 										
deer 										
dog 										
frog 										
horse 										
ship 										
truck
"""

CIFAR10_LABELS = {
    "0": "airplane",
    "1": "automobile",
    "2": "bird",
    "3": "cat",
    "4": "deer",
    "5": "dog",
    "6": "frog",
    "7": "horse",
    "8": "ship",
    "9": "truck"
 }


# Load the data
def load_cifar10(out_dir=""):
    # load data
    out_dir += "\\"
    fashion_mnist = tf.keras.datasets.cifar10
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
    print("x_train.shape:", x_train.shape)
    print("y_train.shape:", y_train.shape)
    print("x_test.shape:", x_test.shape)
    print("x_test.shape:", x_test.shape)
    # display some examples
    plt.clf()
    samles_test = [4865, 5379, 7151]
    for iter in range(3):
        #val = randint(0, 10000)
        val = samles_test[iter]
        print("Cifar10 sample img[", val, "] ", str(y_test[val][0]))
        img_name = "cifar_sample_" + str(val) + "_" + CIFAR10_LABELS[str(y_test[val][0])]
        plt.imshow(x_test[val])
        plt.savefig(out_dir + img_name)
        plt.clf()
    # a maior diferença do cifar para o mnist é que são imagens coloridas
    # então os vetores de entrada são 3d. protanto é necessaria a aplicação da operação de flatten
    # regularization
    x_train, x_test = x_train/255.0, x_test/255.0
    y_train, y_test = y_train.flatten(), y_test.flatten()
    # calc number of classes
    K = len(set(y_train))
    print("number of classes of CIFAR:", K)
    return (x_train, y_train), (x_test, y_test), K

# build the moel using function API
def build_the_model(input_shape, number_of_classes):
    # model hyperparameters
    kernel_size = (3, 3)
    pool_kernel = (2, 3)
    cl1 = 32
    cl2 = 64
    cl3 = 128
    dl1 = 1024
    dl2 = number_of_classes
    strides = 2
    actv_function_conv = 'relu'
    actv_function_dense = 'relu'
    actv_function_out = 'softmax'
    loss_function = 'sparse_categorical_crossentropy'
    optimizer_func = 'adam'
    # changed!
    padding_type = 'same'
    # model build
    i = Input(shape=input_shape)
    # removed!
    # x = Conv2D(cl1, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(i)
    # x = Conv2D(cl2, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(x)
    # x = Conv2D(cl3, kernel_size=kernel_size, strides=strides, activation=actv_function_conv)(x)

    # new !

    # conv Layer 01
    x = Conv2D(cl1, kernel_size=kernel_size, activation=actv_function_conv, padding=padding_type)(i)
    x = BatchNormalization()(x)
    x = Conv2D(cl1, kernel_size=kernel_size, activation=actv_function_conv, padding=padding_type)(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D(pool_kernel)(x)

    # conv Layer 02
    x = Conv2D(cl2, kernel_size=kernel_size, activation=actv_function_conv, padding=padding_type)(x)
    x = BatchNormalization()(x)
    x = Conv2D(cl2, kernel_size=kernel_size, activation=actv_function_conv, padding=padding_type)(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D(pool_kernel)(x)

    # conv Layer 03
    x = Conv2D(cl3, kernel_size=kernel_size, activation=actv_function_conv, padding=padding_type)(x)
    x = BatchNormalization()(x)
    x = Conv2D(cl3, kernel_size=kernel_size, activation=actv_function_conv, padding=padding_type)(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D(pool_kernel)(x)

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
    model.summary()
    return model

def train_the_model(model, x_train, y_train, x_test, y_test, n_epochs):
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)
    return r

def train_the_model_with_data_augumentation(model, x_train, y_train, x_test, y_test, n_epochs):
    batch_size = 32
    data_generator = tf.keras.preprocessing.image.ImageDataGenerator(width_shift_range=0.1,
                                                                     height_shift_range=0.1,
                                                                     horizontal_flip=True)
    train_generator = data_generator.flow(x_train, y_train, batch_size)
    steps_per_epoch = x_train.shape[0] // batch_size
    # note if you run this after calling the previous model.fit it will continue training where it left off
    # UserWarning: `Model.fit_generator` is deprecated and will be removed in a future version. Please use `Model.fit`, which supports generators.
    # r = model.fit_generator(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)
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

def plot_confusion_matrix(model, x_test, y_test, out_dir, n_miss_examples = 1):
    out_dir += "\\"
    p_test = model.predict(x_test).argmax(axis=1)
    cm = confusion_matrix(y_test, p_test)
    Utils.plot_confusion_matrix(cm, list(range(10)), out_file_name= out_dir + "CnnFashionMnist_ConfusionMatrix")
    # show some missclassified examples
    the_labels = LABELS.split()
    misclassified_idx = np.where(p_test != y_test)[0]
    count = 0
    while count < n_miss_examples:
        i = np.random.choice(misclassified_idx)
        print("Missclassified sample: ", i)
        the_title = "TrueLabel: " + the_labels[y_test[i]] + ", Predicted:" + the_labels[p_test[i]]
        print("The Title:", the_title)
        plt.clf()
        plt.imshow(x_test[i])
        plt.title(the_title)
        plt.savefig(out_dir + "missclassified_" + str(count))
        count += 1

def main():
<<<<<<< HEAD
    n_epochs = 50
=======
    n_epochs = 2
>>>>>>> 5a748b3cf980bfc23ba070449ce618cddc168be9
    out_dir = "36"
    (x_train, y_train), (x_test, y_test), K = load_cifar10(out_dir)
    model = build_the_model(input_shape=x_train[0].shape, number_of_classes=K)
    r = train_the_model_with_data_augumentation(model, x_train, y_train, x_test, y_test, n_epochs=n_epochs)
    plot_loss_and_accurary_per_iteration(r, out_dir=out_dir)
    plot_confusion_matrix(model, x_test, y_test, out_dir, 5)

if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()

