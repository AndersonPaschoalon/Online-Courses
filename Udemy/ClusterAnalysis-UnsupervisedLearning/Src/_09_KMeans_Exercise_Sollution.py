import numpy as np
import matplotlib.pyplot as plt


def generate_data_to_cluster(N, D, K):
    mu1 = np.array([0, 0])
    mu2 = np.array([5, 5])
    mu3 = np.array([0, 5])
    X = np.zeros((N, D))
    X[:100, :] = np.random.randn(100, D) + mu1
    X[100:200, :] = np.random.randn(100, D) + mu2
    X[200:, :] = np.random.randn(100, D) + mu3
    Y = np.array([0]*100 + [1]*100 + [2]*100)
    # find the mean of each cluester
    means = np.zeros((K, D))
    means[0, :] = X[Y == 0].mean(axis=0)
    means[1, :] = X[Y == 1].mean(axis=0)
    means[2, :] = X[Y == 2].mean(axis=0)
    return X, Y, means


def sandbox():
    D = 2
    K = 3
    N = 300
    X, Y, means = generate_data_to_cluster(N, D, K)
    print("X.mean(axis=0).shape=", X.mean(axis=0).shape)
    # plot the data
    plt.scatter(X[:, 0], X[:, 1], c=Y)
    # plot the menas with the data
    plt.scatter(means[:, 0], means[:, 1], s=500, c='red', marker='*')
    plt.savefig("09/kmeans_ex01_proposed_sollution")
    plt.show()

if __name__ == '__main__':
    print('PyCharm')
    sandbox()