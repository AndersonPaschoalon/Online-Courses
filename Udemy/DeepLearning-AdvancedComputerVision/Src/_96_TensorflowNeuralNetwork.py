import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pandas as pd
import matplotlib.pyplot

# using tf version 1
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from Utils import Utils

def error_rate(p, t):
    return np.mean(p != t)

def get_normalized_data():
    print("Reading in and transforming data...")

    if not os.path.exists('93/large_files/train.csv'):
        print('Looking for 93/large_files/train.csv')
        print('You have not downloaded the data and/or not placed the files in the correct location.')
        print('Please get the data from: https://www.kaggle.com/c/digit-recognizer')
        print('Place train.csv in the folder large_files adjacent to the class folder')
        exit()

    df = pd.read_csv('93/large_files/train.csv')
    data = df.values.astype(np.float32)
    np.random.shuffle(data)
    X = data[:, 1:]
    Y = data[:, 0]

    Xtrain = X[:-1000]
    Ytrain = Y[:-1000]
    Xtest = X[-1000:]
    Ytest = Y[-1000:]

    # normalize the data
    mu = Xtrain.mean(axis=0)
    std = Xtrain.std(axis=0)
    np.place(std, std == 0, 1)
    Xtrain = (Xtrain - mu) / std
    Xtest = (Xtest - mu) / std

    return Xtrain, Xtest, Ytrain, Ytest

def get_normalized_data_2():
    print("Reading in and transforming data...")

    if not os.path.exists('93/large_files/train.csv'):
        print('Looking for 93/large_files/train.csv')
        print('You have not downloaded the data and/or not placed the files in the correct location.')
        print('Please get the data from: https://www.kaggle.com/c/digit-recognizer')
        print('Place train.csv in the folder large_files adjacent to the class folder')
        exit()

    df = pd.read_csv('93/large_files/train.csv')
    data = df.values.astype(np.float32)
    np.random.shuffle(data)
    Xtrain = data[:, 1:]
    Ytrain = data[:, 0]

    df2 = pd.read_csv('93/large_files/test.csv')
    data2 = df2.values.astype(np.float32)
    np.random.shuffle(data)
    Xtest = data2[:, 1:]
    Ytest = data2[:, 0]

    mu_train = Xtrain.mean(axis=0)
    std_train = Xtrain.std(axis=0)
    np.place(std_train, std_train == 0, 1)
    Xtrain = (Xtrain - mu_train) / std_train

    mu_test = Xtest.mean(axis=0)
    std_test = Xtest.std(axis=0)
    np.place(std_test, std_test == 0, 1)
    Xtest = (Xtest - mu_test) / std_test

    return Xtrain, Xtest, Ytrain, Ytest


def main():
    Xtrain, Xtest, Ytrain, Ytest = get_normalized_data()
    # Xtrain, Xtest, Ytrain, Ytest = get_normalized_data_2()
    print("Xtrain.shape:", Xtrain.shape)
    print("Xtest.shape:", Xtest.shape)
    print("Ytrain.shape:", Ytrain.shape)
    print("Ytest.shape:", Ytest.shape)

    # max_iter = 15
    #max_iter = 20
    #max_iter = 50
    max_iter = 30
    print_period = 50
    # lr = 0.00004
    lr = 0.0000135 # melhor para o otimizador RMSPropOptimizer
    # lr = 0.0004 # melhor para o Adam
    #lr = 0.000009
    # reg = 0.01
    reg = 0.005
    Ytrain_ind = Utils.y2indicator(Ytrain)
    Ytest_ind = Utils.y2indicator(Ytest)
    print("Ytrain_ind.shape:", Ytrain_ind.shape)
    print("Ytest_ind.shape:", Ytest_ind.shape)

    N, D = Xtrain.shape
    # batch_sz = 500
    batch_sz = 1500
    n_batches = N // batch_sz

    # add an extra layer just for fun
    #M1 = 300
    M1 = 400
    #M1 = 1024
    #M2 = 100
    M2 = 200
    #M2 = 512
    K = 10
    print("np.sqrt(D):", np.sqrt(D))
    W1_init = np.random.randn(D, M1) / np.sqrt(D)
    b1_init = np.zeros(M1)
    W2_init = np.random.randn(M1, M2) / np.sqrt(M1)
    b2_init = np.zeros(M2)
    W3_init = np.random.randn(M2, K) / np.sqrt(M2)
    b3_init = np.zeros(K)

    # define variables and expressions
    X = tf.placeholder(tf.float32, shape=(None, D), name='X')
    T = tf.placeholder(tf.float32, shape=(None, K), name='T')
    W1 = tf.Variable(W1_init.astype(np.float32))
    b1 = tf.Variable(b1_init.astype(np.float32))
    W2 = tf.Variable(W2_init.astype(np.float32))
    b2 = tf.Variable(b2_init.astype(np.float32))
    W3 = tf.Variable(W3_init.astype(np.float32))
    b3 = tf.Variable(b3_init.astype(np.float32))

    # define the model
    # the model has two layers of neurons with relu activation functions
    Z1 = tf.nn.relu(tf.matmul(X, W1) + b1)
    Z2 = tf.nn.relu(tf.matmul(Z1, W2) + b2)
    Yish = tf.matmul(Z2, W3) + b3

    # softmax_cross_entropy_with_logits take in the "logits"
    # if you wanted to know the actual output of the neural net,
    # you could pass "Yish" into tf.nn.softmax(logits)
    cost = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits_v2(logits=Yish, labels=T))

    # we choose the optimizer but don't implement the algorithm ourselves
    # let's go with RMSprop, since we just learned about it.
    # it includes momentum!
    train_op = tf.train.RMSPropOptimizer(lr, decay=0.99, momentum=0.9).minimize(cost)
    #train_op = tf.train.AdamOptimizer(learning_rate=lr,
    #                                  beta1=0.8,
    #                                  beta2=0.999,
    #                                  epsilon=1e-08,
    #                                  use_locking=False,
    #                                  name='Adam').minimize(cost)

    # we'll use this to calculate the error rate
    predict_op = tf.argmax(Yish, 1)

    costs = []
    init = tf.global_variables_initializer()
    with tf.Session() as session:
        session.run(init)

        for i in range(max_iter):
            for j in range(n_batches):
                Xbatch = Xtrain[j*batch_sz:(j*batch_sz + batch_sz),]
                Ybatch = Ytrain_ind[j*batch_sz:(j*batch_sz + batch_sz),]

                session.run(train_op, feed_dict={X: Xbatch, T: Ybatch})
                if j % print_period == 0:
                    test_cost = session.run(cost, feed_dict={X:Xtest, T: Ytest_ind})
                    prediction = session.run(predict_op, feed_dict={X: Xtest})
                    err = error_rate(prediction, Ytest)
                    print("Cost/err at iteration i=%d, j=%d %.3f / %0.3f" % (i, j, test_cost, err))
                    costs.append(test_cost)

    plt.clf()
    plt.plot(costs)
    plt.show()




    print("todo")


if __name__ == '__main__':
    print(tf.__version__)
    main()
