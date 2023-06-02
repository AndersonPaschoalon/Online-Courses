from builtins import range, input
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

    plt.plot(costs)
    plt.title("Costs")
    plt.savefig(f"25/{nickname}costs_k{str(K)}_beta{str(beta)}.jpg")
    if show_plots:
        plt.show()
    plt.clf()

    random_colors = np.random.random((K, 3))
    print(random_colors)
    colors = R.dot(random_colors)
    print(colors)
    print("-----------------------------")
    plt.scatter(X[:, 0], X[:, 1], c=colors)
    plt.savefig(f"25/{nickname}scatter_k{str(K)}_beta{str(beta)}.jpg")
    if show_plots:
        plt.show()
    plt.clf()
    return M, R


def get_simple_data():
    # assume 3 means
    D = 2 # so we can visualize it more easily
    s = 4 # separation so we can control how far apart the means are
    mu1 = np.array([0, 0])
    mu2 = np.array([s, s])
    mu3 = np.array([0, s])

    N = 900 # number of samples
    X = np.zeros((N, D))
    X[:300, :] = np.random.randn(300, D) + mu1
    X[300:600, :] = np.random.randn(300, D) + mu2
    X[600:, :] = np.random.randn(300, D) + mu3
    return X


def main():
    show_plt = False
    X = get_simple_data()
    plt.scatter(X[:,0], X[:,1])
    if show_plt:
        plt.show()

    costs = np.empty(10)
    costs[0] = None
    for k in range(1, 10):
        M, R = plot_k_means(X, k, show_plots=show_plt, nickname=f"iter{k}")
        c = cost(X, R, M)
        costs[k] = c

    plt.clf()
    plt.plot(costs)
    plt.title("Cost vs K")
    plt.savefig("25/K_vs_cost")
    if show_plt:
        plt.show()


if __name__ == '__main__':
    main()

