import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def generate_data_to_cluster(cluster, n_data=1000, data_dim=2):
    data_mean = 2*cluster
    sigma = 0.4
    s1 = np.random.normal(data_mean, sigma, n_data)
    s2 = np.random.normal(data_mean, sigma, n_data)
    combined = np.vstack((s1, s2)).T
    return combined


def calc_closest_point(point, array_points):
    distances = np.linalg.norm(array_points - point, axis=1)
    closest_index = np.argmin(distances)
    return closest_index


def calc_closest_cluster(data, centroids):
    n_elements = data.shape[0]
    y = np.zeros(n_elements)
    for i in range(n_elements):
        y[i] = calc_closest_point(data[i], centroids)
    return y


def check_missclassified(y, expected_value, print_label):
    for i in range(y.shape[0]):
        if y[i] != expected_value:
            print(f"{print_label} y[{i}]:{y[i]}, expected_value:{expected_value}")


def add_to_scatterplot_2(x, y):
    a = x[:, 0]
    b = x[:, 1]
    plt.scatter(a, b, c=y)



def add_centroid(centroid, color='black'):
    plt.scatter(centroid[0], centroid[1], marker='*', color=color)


def calc_centroid(data):
    return np.mean(data, axis=0)


def sandbox():
    data0 = generate_data_to_cluster(0, n_data=30)
    data1 = generate_data_to_cluster(1, n_data=30)
    data2 = generate_data_to_cluster(2, n_data=30)
    centroid0 = calc_centroid(data0)
    centroid1 = calc_centroid(data1)
    centroid2 = calc_centroid(data2)
    centroids = np.array([centroid0, centroid1, centroid2])
    y0 = calc_closest_cluster(data0, centroids)
    check_missclassified(y0, 0, "y0 cluster")
    y1 = calc_closest_cluster(data1, centroids)
    check_missclassified(y1, 1, "y1 cluster")
    y2 = calc_closest_cluster(data2, centroids)
    check_missclassified(y2, 2, "y2 cluster")
    X = np.concatenate((data0, data1, data2))
    Y = np.concatenate((y0, y1, y2))
    add_to_scatterplot_2(X, Y)
    print("Centroid of k0 is", centroid0)
    add_centroid(centroid0)
    print("Centroid of k1 is", centroid1)
    add_centroid(centroid1)
    print("Centroid of k2 is", centroid2)
    add_centroid(centroid2)
    plt.savefig("10/kmeans_ex02_result")
    print("end")


if __name__ == '__main__':
    print('PyCharm')
    sandbox()