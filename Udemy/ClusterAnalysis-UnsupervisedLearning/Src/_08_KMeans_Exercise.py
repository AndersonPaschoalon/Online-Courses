import numpy as np
import matplotlib.pyplot as plt


def generate_data_to_cluster(cluster, n_data=1000, data_dim=2):
    data_mean = 2*cluster
    sigma = 0.4
    s1 = np.random.normal(data_mean, sigma, n_data)
    s2 = np.random.normal(data_mean, sigma, n_data)
    combined = np.vstack((s1, s2)).T
    return combined


def add_to_scatterplot(data, color='blue'):
    x = data[:, 0]  # extract the first column as x-coordinates
    y = data[:, 1]  # extract the second column as y-coordinates
    plt.scatter(x, y, color=color)  # make a scatterplot
    #plt.show()  # display the plot

def add_centroid(centroid, color='black'):
    plt.scatter(centroid[0], centroid[1], marker='*', color=color)


def calc_centroid(data):
    return np.mean(data, axis=0)



def sandbox():
    data0 = generate_data_to_cluster(0, n_data=30)
    data1 = generate_data_to_cluster(1, n_data=30)
    data2 = generate_data_to_cluster(2, n_data=30)
    print("Plot Kluster 0")
    add_to_scatterplot(data0)
    print("Plot Kluster 1")
    add_to_scatterplot(data1, color='red')
    print("Plot Kluster 2")
    add_to_scatterplot(data2, color='green')
    print("Plot Kluster")
    centroid0 = calc_centroid(data0)
    centroid1 = calc_centroid(data1)
    centroid2 = calc_centroid(data2)
    print("Centroid of k0 is", centroid0)
    add_centroid(centroid0)
    print("Centroid of k1 is", centroid1)
    add_centroid(centroid1)
    print("Centroid of k2 is", centroid2)
    add_centroid(centroid2)
    plt.savefig("08/kmeans_ex01_result")
    # plt.show()

if __name__ == '__main__':
    print('PyCharm')
    sandbox()