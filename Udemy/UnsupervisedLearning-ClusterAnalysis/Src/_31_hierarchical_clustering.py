import numpy as np
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import dendrogram, linkage

def create_dataaset(N=900, D=2, s=4):
    mu1 = np.array([0, 0])
    mu2 = np.array([s, s])
    mu3 = np.array([0, s])
    X = np.zeros((N, D))
    X[:300, :] = np.random.randn(300, D) + mu1
    X[300:600, :] = np.random.randn(300, D) + mu2
    X[600:, :] = np.random.randn(300, D) + mu3
    return X



def main():
    X = create_dataaset(N=900, D=2, s=4)

    Z = linkage(X, 'ward')
    print("Z.shape:", Z.shape)
    # Z has the format [idx1, idx2, dist, sample_count]
    # therefore, its size will be (N-1, 4)
    # from documentation:
    # A (n-1) by 4 matrix Z is returned. At the i-th iteration,
    # clusters with indices Z[i, 0] and Z[i, 1] are combined to
    # form cluster n + i. A cluster with an index less than n
    # corresponds to one of the original observations.
    # The distance between clusters Z[i, 0] and Z[i, 1] is given
    # by Z[i, 2]. The fourth value Z[i, 3] represents the number
    # of original observations in the newly formed cluster.
    plt.title("Ward")
    dendrogram(Z)
    # plt.show()
    plt.savefig("31/ward")

    Z = linkage(X, 'single')
    plt.title("Single")
    dendrogram(Z)
    # plt.show()
    plt.savefig("31/single")

    Z = linkage(X, 'complete')
    plt.title("Complete")
    dendrogram(Z)
    # plt.show()
    plt.savefig("31/complete")


if __name__ == '__main__':
    main()
