# check tensor flow version
import tensorflow as tf
print("TensorFlow version:", tf.__version__)

# Load in the data
from sklearn.datasets import load_breast_cancer

# split the data into train and test sets
from sklearn.model_selection import train_test_split

# Normalizar os dados
from sklearn.preprocessing import StandardScaler

import numpy as np

from keras import Sequential
from tensorflow import keras

#plotter
import matplotlib.pyplot as plt

# Lesson 09
def test_input_data(data):
    # check the data
    print(type(data))

    print("Print some values to learn about the data...")
    # note: it is a bunch object. basically it acts like a dictionary where you can treat the keys like attributs
    print(data.keys())
    # print(data.values())
    print("======================")
    print(data['DESCR'])
    print("======================")
    print(data['target'])
    print("======================")
    print(data['filename'])

    # data refer to the input values x and targed refer to the output y
    print("")
    print("data x target")
    print("data.data.shape:", data.data.shape)
    print("data.target.shape:", data.target.shape)
    print("data.target_names:", data.target_names)
    print("data.feature_names:", data.feature_names)

# lesson 09
def loading_the_data(test_split):
    # load the data
    data = load_breast_cancer()
    test_input_data(data)
    # split the data into train and test sets
    print("-- split the data into train and test sets")
    x = data.data
    y = data.target
    x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, test_size=test_split)
    # N sample size
    # D number of features
    N, D = x_train.shape
    print("x_train.shape:", x_train.shape)
    print("x_test.shape:", x_test.shape)
    print("-- Normalizar os dados")
    scaller = StandardScaler()
    x_train = scaller.fit_transform(x_train)
    x_test = scaller.transform(x_test)
    return x, y, x_train, x_test, y_train, y_test, N, D

def creating_and_training_the_model(x_train, x_test, y_train, y_test, N, D, n_epochs):
    # now, it is time for tensor flow work
    model = tf.keras.models.Sequential([
     tf.keras.layers.Input(shape=(D,)),
     tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    ## Alternatively, you can do :
    # model = tf.keras.models.Sequential()
    # model.add(tf.keras.layers.Dense(1, input_shape=(D,), activation='sigmoid'))

    # model optimizer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)

    # evaluate the model
    print("Train score: ", model.evaluate(x_train, y_train))
    print("Test score: ", model.evaluate(x_test, y_test))

    #plot what's returned
    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.savefig("09/09_ClassificationNetwork_Error")

    plt.plot(r.history['accuracy'], label='acc')
    plt.plot(r.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.savefig("09/09_ClassificationNetwork_Accuracy")

    return model


# Lesson 14. Making Predictions
def making_predictions(model, X_test, y_test):
    P = model.predict(X_test)
    print(P)

    # Round to get the actual predictions
    # note: has to be flatteded, since the gargets are size (N, ) while the predictions are size (N, 1)
    P = np.round(P).flatten()
    print(P)

    # Claculate the accuracy, compare it to evaluate() output
    # if P == y_test it equals to 1 (right). Divided by the number of elements...
    print("Manually calculated accuracy: ", np.mean(P == y_test))
    print("Evaluate output:", model.evaluate(X_test, y_test))
    # we get the same result as when wo do model.evaluate()

# lesson 15: saving a model
def saving_the_model_and_evaluate(model_name, model, X_test, y_test):
    model.save(model_name + ".h5")
    # Lets load the model and confirm it still works
    model = tf.keras.models.load_model(model_name + ".h5")
    print("model.layers:", model.layers)
    model.evaluate(X_test, y_test)



def main():
    test_split = 0.33
    n_epochs = 100
    x, y, x_train, x_test, y_train, y_test, N, D = loading_the_data(test_split)
    print(x)
    print(x_train)
    print(y)
    model = creating_and_training_the_model(x_train, x_test, y_train, y_test, N, D, n_epochs)
    making_predictions(model, x_test, y_test)
    saving_the_model_and_evaluate("09/linearclassifier", model, x_test, y_test)

if __name__ == '__main__':
    main()