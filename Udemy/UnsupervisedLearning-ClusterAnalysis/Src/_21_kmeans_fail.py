# https://deeplearningcourses.com/c/cluster-analysis-unsupervised-machine-learning-python
# https://www.udemy.com/cluster-analysis-unsupervised-machine-learning-python
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


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
    if show_plots:
        plt.plot(costs)
        plt.title("Costs")
        plt.savefig(f"21/{nickname}costs_k{str(K)}_beta{str(beta)}.jpg")
        plt.show()
        plt.clf()



        random_colors = np.random.random((K, 3))
        print(random_colors)
        colors = R.dot(random_colors)
        print(colors)
        print("-----------------------------")
        plt.scatter(X[:, 0], X[:, 1], c=colors)
        plt.savefig(f"21/{nickname}scatter_k{str(K)}_beta{str(beta)}.jpg")
        plt.show()
        plt.clf()


def donut():
    N = 1000
    D = 2

    R_inner = 5
    R_outer = 10

    # distance from origin is radius + random normal
    # angle theta is uniformly distributed between (0, 2pi)
    R1 = np.random.randn(N//2) + R_inner
    theta = 2*np.pi*np.random.random(N//2)
    X_inner = np.concatenate([[R1 * np.cos(theta)], [R1 * np.sin(theta)]]).T

    R2 = np.random.randn(N//2) + R_outer
    theta = 2*np.pi*np.random.random(N//2)
    X_outer = np.concatenate([[R2 * np.cos(theta)], [R2 * np.sin(theta)]]).T

    X = np.concatenate([ X_inner, X_outer ])
    return X


def main():
    # donut
    X = donut()
    plot_k_means(X, 2, beta=0.1, show_plots=True, nickname="donut")

    # elongated clusters
    X = np.zeros((1000, 2))
    X[:500,:] = np.random.multivariate_normal([0, 0], [[1, 0], [0, 20]], 500)
    X[500:,:] = np.random.multivariate_normal([5, 0], [[1, 0], [0, 20]], 500)
    plot_k_means(X, 2, beta=0.1, show_plots=True, nickname="elongated_clusters")

    # different density
    X = np.zeros((1000, 2))
    X[:950,:] = np.array([0,0]) + np.random.randn(950, 2)
    X[950:,:] = np.array([3,0]) + np.random.randn(50, 2)
    plot_k_means(X, 2, show_plots=True, nickname="different_density")



if __name__ == '__main__':
    main()
