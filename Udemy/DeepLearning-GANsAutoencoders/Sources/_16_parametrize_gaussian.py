import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn

OUT_PATH = ".\\Results\\16\\"

def softplus(x):
    return np.log1p(np.exp(x))

# we are going to make a neural network with the layers sizes (4, 3, 2) like a toy version of a decoder

W1 = np.random.randn(4, 3)
# 2*2 -> one componet for the mean and other for the std
W2 = np.random.randn(3, 2*2)


def forward(x, W1, W2):
    hidden = np.tanh(x.dot(W1))
    output = hidden.dot(W2)
    mean = output[:2]
    stddev = softplus(output[2:])
    return mean, stddev


# random inpout
x = np.random.randn(4)
mean, stddev = forward(x, W1, W2)
print("mean:", mean)
print("stddev:", mean)

samples = mvn.rvs(mean=mean, cov=stddev**2, size=10000)


plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5)
plt.show()

plot_file = os.path.join(OUT_PATH, "scatter_plot_gaussian")
plt.savefig(plot_file)