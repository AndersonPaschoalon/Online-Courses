import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def add_to_scatterplot_2(x, y):
    a = x[:, 0]
    b = x[:, 1]
    plt.scatter(a, b, c=y)


def plt_kmeans_cost_function(J):
    plt.plot(J)


def plot_centroids(kcentroids_history):
    kcenlen = kcentroids_history.shape[0] - 1
    iter = 0
    for x in kcentroids_history:
        nk = x.shape[0]
        for j in range(nk):
            if iter < kcenlen:
                plt.scatter(x[j, 0], x[j, 1], marker='*', color='magenta')
            else:
                plt.scatter(x[j, 0], x[j, 1], marker='*', color='red')
        iter += 1


def generate_data_to_cluster(cluster, n_data=1000):
    data_mean = 2*cluster
    sigma = 0.4
    s1 = np.random.normal(data_mean, sigma, n_data)
    s2 = np.random.normal(data_mean, sigma, n_data)
    combined = np.vstack((s1, s2)).T
    return combined

def generate_data_all_clusters(K, points_by_cluster=100):
    for i in range(K):
        if i == 0:
            data = generate_data_to_cluster(i, n_data=points_by_cluster)
        else:
            gen = generate_data_to_cluster(i, n_data=points_by_cluster)
            data = np.vstack((data, gen))
    return data


def calc_closest_point(point, array_points):
    distances = np.linalg.norm(array_points - point, axis=1)
    closest_index = np.argmin(distances)
    min_distance = distances[closest_index]
    return closest_index, min_distance


def calc_closest_cluster(data, centroids):
    n_elements = data.shape[0]
    # clusters indexes
    y = np.full((n_elements), -1)
    # cost function
    j_vec = np.zeros(n_elements)
    for i in range(n_elements):
        y[i], j_vec[i] = calc_closest_point(data[i], centroids)
    j_summ = np.sum(j_vec)
    return y, j_summ


def calc_initial_centroids(K, Data):
    max_val = np.amax(Data)
    min_val = np.amin(Data)
    x1 = np.random.uniform(min_val, max_val, size=K)
    x2 = np.random.uniform(min_val, max_val, size=K)
    kcentroids = np.vstack((x1, x2)).T
    #kcentroids = np.random.uniform(min_val, max_val, size=K)
    return kcentroids


def calc_cluster_centroids(Y, Data, K):
    kcentroids = np.zeros((K, 2))
    for i in range(K):
        if Data[Y == i].shape[0] > 0:
            c = Data[Y == i].mean(axis=0)
        else:
            c = np.zeros((1, 2))
        kcentroids[i, :] = c
    return kcentroids


def kmeans(K, Data):
    kcentroids = calc_initial_centroids(K, Data)
    n_elements = Data.shape[0]
    # cluster array
    Y = np.full((n_elements), -1)
    # cost function
    J = np.empty((0,))
    Ylast = Y
    iter = 0
    while True:
        # Assign cluster identities based on current cluster centers
        Y, Jiter = calc_closest_cluster(Data, kcentroids)
        J = np.append(J, [Jiter])
        # Calculate cluster centers based on cluster identities
        kcentroids = calc_cluster_centroids(Y, Data, K)
        if iter == 0:
            kcentroids_history = [kcentroids]
        else:
            kcentroids_history = np.append(kcentroids_history, [kcentroids], axis=0)
            #  np.vstack((kcentroids_history, kcentroids))
        print("iter ", iter)
        if np.array_equal(Ylast, Y):
            print("Ylast == Y ")
            print("Y:", Y)
            print("Ylast:", Ylast)
            print("kcentroids_history:", kcentroids_history)
            break
        Ylast = Y
        iter += 1
    print("J: ", J)
    return Y, kcentroids, kcentroids_history, J


def sandbox():
    D = 2
    K = 3
    N = 300
    X = generate_data_all_clusters(K=K, points_by_cluster=100)
    Y, kcentroids, kcentroids_history, J = kmeans(K, X)

    # Plot centroids
    plt.clf()
    add_to_scatterplot_2(x=X, y=Y)
    plot_centroids(kcentroids_history)
    plt.savefig("12/scatterplot")

    #plot cost function
    plt.clf()
    plt_kmeans_cost_function(J)
    plt.savefig("12/kmeans-cost-function")



if __name__ == '__main__':
    print('PyCharm')
    sandbox()
