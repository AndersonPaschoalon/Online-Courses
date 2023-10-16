# https://deeplearningcourses.com/c/cluster-analysis-unsupervised-machine-learning-python
# https://www.udemy.com/cluster-analysis-unsupervised-machine-learning-python
from builtins import range, input
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances


def d(u, v):
    """
    Evaluates the Euclidiand distances between two numpy arrays u adn v.
    :param u:
    :param v:
    :return:
    """
    diff = u - v
    return diff.dot(diff)


def cost(X, R, M):
    cost = 0
    for k in range(len(M)):
        # method 1 - not vectorized
        # for n in range(len(X)):
        #     cost += R[n, k]*d(M[k], X[n])

        #method 2  - vectorized
        diff = X - M[k]
        sq_distances = (diff * diff).sum(axis=1)
        cost += (R[:, k] * sq_distances).sum()
    return cost


def plot_k_means(X, K, max_iter=20, beta=1.0, show_plots=True):
    N, D = X.shape
    M = np.zeros((K, D))
    R = np.ones((N, K)) / K

    for k in range(K):
        M[k] = X[np.random.choice(N)]

    #grid_width = 5
    #grid_height = max_iter / grid_width
    #random_colors = np.random.random((K, 3))
    #plt.figure()

    costs = np.zeros(max_iter)
    k = 0
    for i in range(max_iter):

        # move the plot inside the for loop
        #colors = R.dot(random_colors)
        #plt.subplot(grid_width, int(grid_height), i+1)

        # step 1: determine assingments / responsabilities
        # is this inefficent?
        for k in range(K):
            for n in range(N):
                R[n, k] = np.exp(-beta * d(M[k], X[n])) / np.sum(np.exp(-beta * d(M[j], X[n])) for j in range(K))

        # step 2: recalculate means
        for k in range(K):
            M[k] = R[:, k].dot(X) / R[:, k].sum()

        costs[i] = cost(X, R, M)
        if i > 0:
            if np.abs(costs[i] - costs[i-1]) < 1e-5:
                break
    if show_plots:
        plt.plot(costs)
        plt.title("Costs")
        plt.savefig("18/costs_k" + str(K) + "_beta" + str(beta) + ".jpg")
        plt.show()
        plt.clf()



        random_colors = np.random.random((K, 3))
        print(random_colors)
        colors = R.dot(random_colors)
        print(colors)
        print("-----------------------------")
        plt.scatter(X[:, 0], X[:, 1], c=colors)
        plt.savefig("18/scatter_k" + str(K) + "_beta" + str(beta) + ".jpg")
        plt.show()
        plt.clf()



def main():
    D = 2
    s = 4
    mu1 = np.array([0, 0])
    mu2 = np.array([5, 5])
    mu3 = np.array([0, 5])
    N = 900
    X = np.zeros((N, D))
    X[:300, :] = np.random.randn(300, D) + mu1
    X[300:600, :] = np.random.randn(300, D) + mu2
    X[600:, :] = np.random.randn(300, D) + mu3

    plt.scatter(X[:, 0], X[:, 1])
    plt.savefig("18/before_kmeans")
    plt.show()
    plt.clf()

    K = 3
    plot_k_means(X, K)

    K = 5
    plot_k_means(X, K)
    #
    K = 5
    plot_k_means(X, K, max_iter=30, beta=0.3)



if __name__ == '__main__':
    main()
