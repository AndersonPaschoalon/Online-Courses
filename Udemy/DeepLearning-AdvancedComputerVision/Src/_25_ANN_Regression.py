import tensorflow as tf
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def make_the_dataset(out_dir):
    # implements the function y = cos(2*x1) + cos(3*x2)
    N = 1000
    X = np.random.random((N, 2)) * 6 - 3 # uniform distributed between (-3, +3)
    Y = np.cos(2*X[:, 0]) + np.cos(3*X[:, 1])
    # plot it
    out_dir = out_dir + "\\"
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:,0], X[:, 1], Y)
    # plt.show()
    plt.savefig(out_dir + "dataset_plot")
    return N, X, Y


def build_the_model(X, Y, n_epochs, n_neurons_l1, input_shape, activation_l1, loss_function, out_dir):
    # build the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(n_neurons_l1, input_shape=input_shape, activation=activation_l1),
        tf.keras.layers.Dense(1)
    ])
    # compile the model
    opt = tf.keras.optimizers.Adam(0.01)
    model.compile(optimizer=opt, loss=loss_function)
    #model.compile(optimizer='adam', loss=loss_function)
    r = model.fit(X, Y, epochs=n_epochs)
    # Plot the Loss
    out_dir = out_dir + "\\"
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.savefig(out_dir + "model_loss_per_iteration")
    return model


def plot_the_prediction_surface(X, Y, model, out_dir):
    # plot the prediction surface
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], Y)
    # surface plot
    out_dir = out_dir + "\\"
    line = np.linspace(-3, 3, 50)
    xx, yy = np.meshgrid(line, line)
    Xgrid = np.vstack((xx.flatten(), yy.flatten())).T
    Yhat = model.predict(Xgrid).flatten()
    ax.plot_trisurf(Xgrid[:, 0], Xgrid[:, 1], Yhat, linewidth=0.2, antialiased=True)
    # plt.show()
    plt.savefig(out_dir + "surface_plot")
    # can it extrapolate?
    # Plot the prediction surface
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], Y)
    # surface plot
    # check if the NN can extrapolate the results
    line = np.linspace(-5, 5, 50)
    xx, yy = np.meshgrid(line, line)
    Xgrid = np.vstack((xx.flatten(), yy.flatten())).T
    Yhat = model.predict(Xgrid).flatten()
    ax.plot_trisurf(Xgrid[:, 0], Xgrid[:, 1], Yhat, linewidth=0.2, antialiased=True)
    plt.savefig(out_dir + "nn_extrapolation")


def main():
    # Make the dataset
    out_dir="25"
    loss_function = 'mse'
    activation_l1 = 'relu'
    input_shape = (2, )
    n_neurons_l1 = 128
    n_epochs = 100
    N, X, Y = make_the_dataset(out_dir)
    model = build_the_model(X, Y, n_epochs, n_neurons_l1, input_shape, activation_l1, loss_function, out_dir=out_dir)
    plot_the_prediction_surface(X, Y, model, out_dir)

if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()
