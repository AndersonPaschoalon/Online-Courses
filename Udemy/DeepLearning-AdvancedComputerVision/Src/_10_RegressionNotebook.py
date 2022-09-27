# check tensor flow version
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# local utility
from Utils import Utils

# Lesson 10
def loading_the_date():
    # download the data
    Utils.wget_if_not_exit("https://raw.githubusercontent.com/lazyprogrammer/machine_learning_examples/master/tf2.0/moore.csv",
                           "10/moore.csv")
    # load the data
    data = pd.read_csv('10/moore.csv', header=None).values
    X = data[:,0].reshape(-1, 1) # make it a 2d arrya of size XxD, where D=1
    Y = data[:,1]
    # print(X)
    # print(Y)
    plt.scatter(X, Y)
    plt.savefig("10/scatter_raw.png")
    # plt.show()
    Y = np.log(Y)
    plt.clf()
    plt.scatter(X, Y)
    plt.savefig("10/scatter_log.png")
    # plt.show()
    X = X - X.mean()
    return X, Y

# Lesson 10
def create_the_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(1,)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer=tf.keras.optimizers.SGD(0.001, 0.9), loss='mse')
    return model

# Lesson 10
def schedule(epoch, lr):
    if epoch >= 50:
        return 0.0001
    return 0.001

# Lesson 10
def fit_the_model(model, X, Y, number_epochs):
    scheduler = tf.keras.callbacks.LearningRateScheduler(schedule)
    r = model.fit(X, Y, epochs=number_epochs, callbacks=[scheduler])
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.savefig("10/learning_rate.png")
    # plt.show()
    print("model.layers=", model.layers)
    print("model.layers[0].get_weights()=", model.layers[0].get_weights())
    a = model.layers[0].get_weights()[0][0,0]
    print("Curve slope is a=", a)

# Lesson 14: making predictions
def making_predictions(model, X, Y):
    # make sure the line fits our data
    Yhat = model.predict(X).flatten()
    plt.clf()
    plt.scatter(X, Y)
    plt.plot(X, Yhat, color='red')
    plt.savefig("10/plot_model.png")
    # Manual Calculation
    # Get the weeights
    w, b = model.layers[0].get_weights()
    # reshape X, because flattened is again earlier
    X = X.reshape(-1, 1)
    # (N x 1) x (1 x 1) + 1 -> (N x 1)
    Yhat2 = (X.dot(w) + b).flatten()
    ret = np.allclose(Yhat, Yhat2)
    print("np.allclose:", ret)



def main():
    number_epochs = 200
    X, Y = loading_the_date()
    model = create_the_model()
    fit_the_model(model, X, Y, number_epochs)
    making_predictions(model, X, Y)
    """
    scheduler = tf.keras.callbacks.LearningRateScheduler(schedule)
    r = model.fit(X, Y, epochs=200, callbacks=[scheduler])
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.savefig("10/learning_rate.png")
    # plt.show()
    print("model.layers=", model.layers)
    print("model.layers[0].get_weights()=", model.layers[0].get_weights())
    a = model.layers[0].get_weights()[0][0,0]
    print("Curve slope is a=", a)
    """






if __name__ == '__main__':
    main()