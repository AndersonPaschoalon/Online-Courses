# https://deeplearningcourses.com/c/cluster-analysis-unsupervised-machine-learning-python
# https://www.udemy.com/cluster-analysis-unsupervised-machine-learning-python

# data is from https://www.kaggle.com/c/digit-recognizer
# each image is a D = 28x28 = 784 dimensional vector
# there are N = 42000 samples
# you can plot an image by reshaping to (28,28) and using plt.imshow()

from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def get_data(limit=None):
    print("Reading in and transforming data...")
    df = pd.read_csv("digit-recognizer/train.csv")
    data = df.values
    np.random.shuffle(data)
    X = data[:, 1:] / 255.0 # data is from 0->255
    Y = data[:, 0]
    if limit is not None:
        X, Y = X[:limit], Y[:limit]
    return X, Y


# hard labels
def purity2(Y, R):
    # maximum purity is 1, highter is better
    C = np.argmax(R, axis=1)
    N = len(Y) # number of data ppoints
    K = len(set(Y)) # number of labels
    total = 0.0
    for k in range(K):
        max_intersection = 0
        for j in range(K):
            intersection = ((C == k) & (Y == j)).sum()
            if intersection > max_intersection:
                max_intersection = intersection
        total += max_intersection
    return total / N


def purity(Y, R):
    # maximum purity is 1, higher is better
    N, K = R.shape
    p = 0
    for k in range(K):
        best_target = -1 # we don't strictly need to store this
        max_intersection = 0
        for j in range(K):
            intersection = R[Y==j, k].sum()
            if intersection > max_intersection:
                max_intersection = intersection
                best_target = j
        p += max_intersection
    return p / N


# hard labels
def DBI2(X, R):
    N, D = X.shape
    _, K = R.shape
    # get sigmas, means first
    sigma = np.zeros(K)
    M = np.zeros((K, D))
    assignments = np.argmax(R, axis=1)
    for k in range(K):
        Xk = X[assignments == k]
        M[k] = Xk.mean(axis=0)
        # assert(Xk.mean(axis=0).shape == (D,))
        n = len(Xk)
        diffs = Xk - M[k]
        sq_diffs = diffs * diffs
        sigma[k] = np.sqrt( sq_diffs.sum() / n )
    # calculate Davies-Bouldin Index
    dbi = 0
    for k in range(K):
        max_ratio = 0
        for j in range(K):
            if k != j:
                numerator = sigma[k] + sigma[j]
                denominator = np.linalg.norm(M[k] - M[j])
                ratio = numerator / denominator
                if ratio > max_ratio:
                    max_ratio = ratio
        dbi += max_ratio
    return dbi / K


def DBI(X, M, R):
    # ratio between sum of std deviations between 2 clusters / distance between cluster means
    # lower is better
    N, D = X.shape
    K, _ = M.shape
    # get sigmas first
    sigma = np.zeros(K)
    for k in range(K):
        diffs = X - M[k] # should be NxD
        squared_distances = (diffs * diffs).sum(axis=1) # now just N
        weighted_squared_distances = R[:,k]*squared_distances
        sigma[k] = np.sqrt( weighted_squared_distances.sum() / R[:,k].sum() )
    # calculate Davies-Bouldin Index
    dbi = 0
    for k in range(K):
        max_ratio = 0
        for j in range(K):
            if k != j:
                numerator = sigma[k] + sigma[j]
                denominator = np.linalg.norm(M[k] - M[j])
                ratio = numerator / denominator
                if ratio > max_ratio:
                    max_ratio = ratio
        dbi += max_ratio
    return dbi / K


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


def plot_k_means(X, K, max_iter=20, beta=1.0, show_plots=True, nickname=""):
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

    plt.plot(costs)
    plt.title("Costs")
    plt.savefig(f"24/{nickname}costs_k{str(K)}_beta{str(beta)}.jpg")
    if show_plots:
        plt.show()
    plt.clf()

    random_colors = np.random.random((K, 3))
    print(random_colors)
    colors = R.dot(random_colors)
    print(colors)
    print("-----------------------------")
    plt.scatter(X[:, 0], X[:, 1], c=colors)
    plt.savefig(f"24/{nickname}scatter_k{str(K)}_beta{str(beta)}.jpg")
    if show_plots:
        plt.show()
    plt.clf()
    return M, R


def main():
    X, Y = get_data(1000)
    # simple data
    # X = get_simple_data()
    # Y = np.array([0]*300 + [1]*300 + [2]*300)

    print(f"Number of data points: {len(Y)}")
    M, R = plot_k_means(X, len(set(Y)), show_plots=False)
    print(f"Purity: {purity(Y, R)}")
    print(f"DBI: {DBI(X, M, R)}")


    print("main")

if __name__ == '__main__':
    main()