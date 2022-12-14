"""
== EXERCÍCIO ==

Classificar imagens do dataset MNIST utilizando regressão linear, nas seguintes categorias:

1) Classificar entre 10 digitos

2) Numeros Pares vs Impares:
    - 0, 2, 4, 6, 8,
    - 1, 3, 5, 7, 9
3) Numeros arredondados vs retos:
    - 0, 2, 3, 5, 6, 8, 9
    - 1, 4, 7
4) Numeros maiories ou iguais a 5
    - 0, 1, 2, 3, 4
    - 5, 6, 7, 8, 9


Utilizar os seguintes modelos:

1) Regressão Linear
2) Rede Neural NPL
3) Vgg19

Para cada caso, plotar:

1) Acurácia
2) Erro
3) Matriz de confusão
4) Exemplos de sucesso e erro.



"""
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import itertools
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout, GlobalMaxPooling2D
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from Utils import Utils

# Constants
EX_01_FOLDER = "Ex_01/"


########################################################################################################################
# Helper functions
########################################################################################################################


class TrainDataset:
    def __init__(self):
        self.input_shape = ()
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.y_train_mnist = []
        self.y_test_mnist = []
        self.labels = []

    def y_mnist(self):
        return self.y_train_mnist, self.y_test_mnist


def _load_in_the_data():
    """
    Load mnist dataset
    :return:
    """
    img_normalization = 255.0
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / img_normalization, x_test / img_normalization
    # This will print (60000, 28, 28)
    # x_train is a vector of 60k images of 28x28 pixels
    print("x_train.shape:", x_train.shape)
    print("x_test.shape:", x_test.shape)
    return x_train, y_train, x_test, y_test


########################################################################################################################
# Create the datasets
########################################################################################################################

def dataset_classification_odd_or_even():
    x_train, y_train_mnist, x_test, y_test_mnist = _load_in_the_data()
    # crete empty arrays fro the labels
    y_train_size = y_train_mnist.size
    y_test_size = y_test_mnist.size
    y_train = np.array([0] * y_train_size)
    y_test = np.array([0] * y_test_size)
    labels = ["even", "odd"]
    img_dimentions = (28, 28)
    i = 0
    for x in y_train_mnist:
        if x % 2 == 1:
            y_train[i] = 1
        print("x:", x, ", y_train[i]:", y_train[i])
        i += 1
    i = 0
    for x in y_test_mnist:
        if x % 2 == 1:
            y_test[i] = 1
        i += 1
    return x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist


def dataset_classification_shape():
    x_train, y_train_mnist, x_test, y_test_mnist = _load_in_the_data()
    # crete empty arrays fro the labels
    y_train_size = y_train_mnist.size
    y_test_size = y_test_mnist.size
    y_train = np.array([0] * y_train_size)
    y_test = np.array([0] * y_test_size)
    labels = ["straight", "rounded"]
    img_dimentions = (28, 28)
    i = 0
    for x in y_train_mnist:
        if x == 0 or x == 2 or x == 3 or x == 5 or x == 6 or x == 8 or x == 9:
            y_train[i] = 1
        # print("x:", x, ", y_train[i]:", y_train[i])
        i += 1
    i = 0
    for x in y_test_mnist:
        if x == 0 or x == 2 or x == 3 or x == 5 or x == 6 or x == 8 or x == 9:
            y_test[i] = 1
        i += 1
    i = 0
    # print("----- ", x_train.shape)
    y_train = np.asarray(y_train).astype('float32').reshape((-1, 1))
    y_test = np.asarray(y_test).astype('float32').reshape((-1, 1))
    return x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist


def dataset_classification_larger_or_eq_5():
    x_train, y_train_mnist, x_test, y_test_mnist = _load_in_the_data()
    # crete empty arrays fro the labels
    y_train_size = y_train_mnist.size
    y_test_size = y_test_mnist.size
    y_train = np.array([0] * y_train_size)
    y_test = np.array([0] * y_test_size)
    labels = ["small", "large"]
    img_dimentions = (28, 28)
    i = 0
    for x in y_train_mnist:
        if x >= 5:
            y_train[i] = 1
        i += 1
    i = 0
    for x in y_test_mnist:
        if x >= 5:
            y_test[i] = 1
        i += 1
    return x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist


def dataset_classification_numbers():
    return _load_in_the_data()


########################################################################################################################
# Build the models
########################################################################################################################


def build_the_model_linear_regression(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    # model optimizer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def build_the_model_mlp(input_shape):
    dl1 = 100
    dl2 = 200
    func_dense = 'relu'
    func_out = 'sigmoid'
    model_optimizer = 'adam'
    cost_function = 'binary_crossentropy'
    set_of_metrics = ['accuracy']
    dropout_percentage = 0.2
    i = Input(shape=input_shape)
    x = Flatten()(i)
    x = Dense(dl1, activation=func_dense)(x)
    x = Dropout(dropout_percentage)(x)
    x = Dense(dl2, activation=func_dense)(x)
    x = Dense(1, activation=func_out)(x)
    model = Model(i, x)
    # Compile the model
    model.compile(optimizer=model_optimizer,
                  loss=cost_function,
                  metrics=set_of_metrics)
    return model


def fit_the_model_linear_regression(input_shape, x_train, y_train, x_test, y_test, n_epochs):
    model = build_the_model_linear_regression(input_shape)
    # Train the model
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)

    # evaluate the model
    print("Train score: ", model.evaluate(x_train, y_train))
    print("Test score: ", model.evaluate(x_test, y_test))

    # plot what's returned
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.savefig(EX_01_FOLDER + "LR_ClassificationNetwork_Error")

    plt.clf()
    plt.plot(r.history['accuracy'], label='acc')
    plt.plot(r.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.savefig(EX_01_FOLDER + "LR_ClassificationNetwork_Accuracy")


def fit_the_model_mpl(input_shape, x_train, y_train, x_test, y_test, y_mnist, list_labels, n_epochs):
    model = build_the_model_mlp(input_shape)
    # Train the model
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)

    # evaluate the model
    print("Train score: ", model.evaluate(x_train, y_train))
    print("Test score: ", model.evaluate(x_test, y_test))

    # plot what's returned
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.savefig(EX_01_FOLDER + "MPL_ClassificationNetwork_Error")

    plt.clf()
    plt.plot(r.history['accuracy'], label='acc')
    plt.plot(r.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.savefig(EX_01_FOLDER + "MPL_ClassificationNetwork_Accuracy")

    # make predictions
    print("Making some predictions...")
    (y_train_mnist, y_test_mnist) = y_mnist
    P = model.predict(x_test)
    P = np.round(P).flatten()
    # print 100 predictions
    for i in range(15):
        print("Prediction: ", P[i], ", Actual:", y_test[i], ", Mnist Value:", y_test_mnist[i])

    # show some misclassified examples
    the_labels = list_labels
    p_test = P

    misclassified_idx = []
    for i in range(len(p_test)):
        if p_test[i] != y_test[i]:
            misclassified_idx.append(i)
    print("misclassified_idx:", misclassified_idx)

    # confusion matrix
    cm = confusion_matrix(y_test, p_test)
    print("list_labels:", list_labels)
    Utils.plot_confusion_matrix(cm, list_labels, out_file_name=EX_01_FOLDER + "mpl_confusion_matrix")
    print("Confusion Matrix:", cm)

    count = 0
    n_miss_examples = 5
    i = 0
    while count < n_miss_examples:
        i = np.random.choice(misclassified_idx)
        print("Misclassified sample: ", i)
        the_title = "TrueLabel: " + the_labels[int(y_test[i])] + ", Predicted:" + the_labels[
            int(p_test[i])], ", Mnist:" + str(y_test_mnist[i])
        print("The Title:", the_title)
        plt.clf()
        plt.imshow(x_test[i])
        plt.title(the_title)
        plt.savefig(EX_01_FOLDER + "misclassified_" + "shape_mlp" + str(count))
        count += 1


def fit_the_model_and_test(model,
                           model_name,
                           classification_dataset,
                           train_dataset: TrainDataset,
                           n_epochs):
    #model = build_the_model_mlp(train_dataset.input_shape)
    # Train the model
    file_prefix = model_name + "_" + classification_dataset
    r = model.fit(train_dataset.x_train,
                  train_dataset.y_train,
                  validation_data=(train_dataset.x_test, train_dataset.y_test),
                  epochs=n_epochs)

    # evaluate the model
    print("Train score: ", model.evaluate(train_dataset.x_train, train_dataset.y_train))
    print("Test score: ", model.evaluate(train_dataset.x_test, train_dataset.y_test))

    # plot what's returned
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.savefig(EX_01_FOLDER + file_prefix + "_ClassificationNetwork_Error")

    plt.clf()
    plt.plot(r.history['accuracy'], label='acc')
    plt.plot(r.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.savefig(EX_01_FOLDER + file_prefix + "_ClassificationNetwork_Accuracy")

    # make predictions
    print("Making some predictions...")
    (y_train_mnist, y_test_mnist) = train_dataset.y_mnist()
    P = model.predict(train_dataset.x_test)
    P = np.round(P).flatten()
    # print 100 predictions
    for i in range(15):
        print("Prediction: ", P[i], ", Actual:", train_dataset.y_test[i], ", Mnist Value:", y_test_mnist[i])

    # show some misclassified examples
    the_labels = train_dataset.labels
    p_test = P

    misclassified_idx = []
    for i in range(len(p_test)):
        if p_test[i] != train_dataset.y_test[i]:
            misclassified_idx.append(i)
    print("misclassified_idx:", misclassified_idx)

    # confusion matrix
    cm = confusion_matrix(train_dataset.y_test, p_test)
    print("train_dataset.labels:", train_dataset.labels)
    Utils.plot_confusion_matrix(cm,
                                train_dataset.labels,
                                out_file_name=EX_01_FOLDER + file_prefix + "_confusion_matrix")
    print("Confusion Matrix:", cm)

    count = 0
    n_miss_examples = 5
    i = 0
    while count < n_miss_examples:
        i = np.random.choice(misclassified_idx)
        print("Misclassified sample: ", i)
        print("int(train_dataset.y_test[i]):", int(train_dataset.y_test[i]))
        print("the_labels[int(train_dataset.y_test[i])]:", the_labels[int(train_dataset.y_test[i])])
        print("int(p_test[i]):", int(p_test[i]))
        print("the_labels[int(p_test[i])]:", the_labels[int(p_test[i])])

        the_title = "TrueLabel: " + the_labels[int(train_dataset.y_test[i])] + ", Predicted:" + the_labels[
            int(p_test[i])], ", Mnist:" + str(y_test_mnist[i])
        print("The Title:", the_title)
        plt.clf()
        plt.imshow(train_dataset.x_test[i])
        plt.title(the_title)
        plt.savefig(EX_01_FOLDER + file_prefix + "misclassified_" + str(count))
        count += 1


def run_test(model_name, classification_dataset, n_epochs):
    td = TrainDataset()
    if classification_dataset == "shape":
        x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist = \
            dataset_classification_shape()
    elif classification_dataset == "odd_or_even":
        x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist = \
            dataset_classification_odd_or_even()
    else:
        x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist = \
            dataset_classification_odd_or_even()
    td.x_train = x_train
    td.y_train = y_train
    td.x_test = x_test
    td.y_test = y_test
    td.labels = labels
    td.img_dimentions = img_dimentions
    td.y_train_mnist = y_train_mnist
    td.y_test_mnist = y_test_mnist
    model = None
    if model_name == "mlp":
        model = build_the_model_mlp(td.img_dimentions)
        model.summary()
        fit_the_model_and_test(model=model,
                               model_name=model_name,
                               classification_dataset=classification_dataset,
                               train_dataset=td,
                               n_epochs=n_epochs)


def main():
    """
    x_train, y_train, x_test, y_test, labels, img_dimentions, y_train_mnist, y_test_mnist = dataset_classification_shape()
    n_epochs = 2
    # fit_the_model_linear_regression(input_shape=img_dimentions,
    #                                x_train=x_train,
    #                                y_train=y_train,
    #                                x_test=x_test,
    #                                y_test=y_test,
    #                                n_epochs=n_epochs)
    fit_the_model_mpl(input_shape=img_dimentions,
                      x_train=x_train,
                      y_train=y_train,
                      x_test=x_test,
                      y_test=y_test,
                      y_mnist=(y_train_mnist, y_test_mnist),
                      list_labels=labels,
                      n_epochs=n_epochs)
    """
    #run_test(model_name="mlp", classification_dataset="shape", n_epochs=2)
    run_test(model_name="mlp", classification_dataset="odd_or_even", n_epochs=2)

if __name__ == '__main__':
    main()
