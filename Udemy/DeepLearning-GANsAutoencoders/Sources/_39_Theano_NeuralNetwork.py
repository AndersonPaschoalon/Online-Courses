import os
import numpy as np
import theano
import theano.tensor as T
import matplotlib.pyplot as plt
# from util import get_normalized_data, y2indicator

out_dir = ".\\Results\\39"


def error_rate(p, t):
    return np.mean(p != t)


def relu(a):
    return a * (a > 0)


def main():
    # step 1: get the data and define all the usual variables
    max_iter = 20
    print_period = 10
    lr = 0.00004
    reg = 0.01

    Xtrain, Xtest, Ytrain, Ytest = get_normalized_data()

    Ytrain_ind = y2indicator(Ytrain)
    Ytest_ind = y2indicator(Ytest)
    N, D = Xtrain.shape
    batch_size = 500
    n_batches = N / batch_size
    M = 300
    K = 10
    W1_init = np.random.randn(D, M) / 28
    b1_init = np.zeros(M)
    W2_init = np.random.randn(M, K) / np.sqrt(M)
    b2_init = np.zeros(K)

    # step 2: define theano variables and expressions
    thX = T.matrix('X')
    thT = T.matrix('T')
    W1 = theano.shared(W1_init, 'W1')
    b1 = theano.shared(b1_init, 'b1')
    W2 = theano.shared(W2_init, 'W2')
    b2 = theano.shared(b2_init, 'b2')

    thZ = relu(thX.dot(W1) + b1)
    thY = T.nnet.softmax(thZ.dot(W2) + b2)

    # define the cost function and prediction
    cost = -(thT * T.log(thY)).sum() + reg*((W1*W1).sum() + (b1*b1).sum() + (W2*W2).sum() + (b2*b2).sum())
    prediction = T.argmax(thY, axis=1)


    # step 3: training expressions and functions
    # we can just include regularization as part of the cost because it is also automatically differentiated!
    update_W1 = W1 - lr*T.grad(cost, W1)
    update_b1 = b1 - lr*T.grad(cost, b1)
    update_W2 = W2 - lr*T.grad(cost, W2)
    update_b2 = b2 - lr*T.grad(cost, b2)

    train = theano.function(
        inputs=[thX, thT],
        updates=[(W1, update_W1), (b1, update_b1), (W2, update_W2), (b2, update_b2)],
    )

    # create another function for this because we want it over the whole dataset
    get_prediction = theano.function(
        inputs=[thX, thT],
        outputs=[cost, prediction],
    )

    costs = []
    for i in range(max_iter):
        for j in range(n_batches):
            Xbatch = Xtrain[j*batch_size:(j*batch_size + batch_size),]
            Ybatch = Ytrain_ind[j*batch_size:(j*batch_size + batch_size),]

            train(Xbatch, Ybatch)
            if j % print_period == 0:
                cost_val, prediction_val = get_prediction(Xtest, Ytest_ind)
                err = error_rate(prediction_val, Ytest)
                print("Cost / err at iteration i=%d, j=%d: %.3f / %.3f" % (i, j, cost_val, err))
                costs.append(cost_val)

    plt.clf()
    plt.plot(costs)
    plt.savefig(os.path.join(out_dir, "costs"))


if __name__ == '__main__':
    main()
