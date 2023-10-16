from __future__ import print_function, division
import os
from builtins import range, input
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn
from sklearn.mixture import BayesianGaussianMixture
import util

OUT_DIR = "Results/08/"


class BayesClassifier:

    def fit(self, X, Y):
        # assume classes are numbered 0...K-1
        self.K = len(set(Y))
        self.gaussians = []

        for k in range(self.K):
            print(f"Fitting GMM {k}")
            Xk = X[Y == k]
            # number of clusters?
            gmm = BayesianGaussianMixture(n_components=10)
            gmm.fit(Xk)
            self.gaussians.append(gmm)

    def sample_given_y(self, y):
        gmm = self.gaussians[y]
        sample = gmm.sample()
        # note: sample returns a tuple containing 2 things:
        # 1) the sample
        # 2) wich cluster it came from
        # We'll use (2) to obtain the means so we can plot
        # them like we did in the previous script
        mean = gmm.means_[sample[1]]
        return sample[0].reshape(28, 28), mean.reshape(28, 28)

    def sample(self):
        y = np.random.randint(self.K)
        return self.sample_given_y(y)


if __name__ == '__main__':
    ret, X, Y = util.get_mnist()
    if not ret:
        exit(1)
    clf = BayesClassifier()
    clf.fit(X, Y)

    for k in range(clf.K):
        # show one sample for each class
        # also show the mean image learned
        sample, mean = clf.sample_given_y(k)

        plt.subplot(1, 2, 1)
        plt.imshow(sample, cmap='gray')
        plt.title("Sample")
        plt.subplot(1, 2, 2)
        plt.imshow(mean, cmap='gray')
        plt.title("Mean")
        plt.savefig(f"{OUT_DIR}SampleAndMean_{k}")

    # generate a random sample
    sample, mean = clf.sample()
    plt.subplot(1, 2, 1)
    plt.imshow(sample, cmap='gray')
    plt.title("Random Sample from Random Class")
    plt.subplot(1, 2, 2)
    plt.imshow(mean, cmap='gray')
    plt.title("Corresponding Cluster Mean")
    plt.savefig(f"{OUT_DIR}RandomSampleFromRandomClass")





