import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

D = 2
K = 3
N = 300

mu1 = np.array([0, 0])
mu2 = np.array([5, 5])
mu3 = np.array([0, 5])

X = np.zeros((N, D))
X[:100, :] = np.random.randn(100, D) + mu1
X[100:200, :] = np.random.randn(100, D) + mu2
X[200:, :] = np.random.randn(100, D) + mu3

# what does the data look like by itself?
# in reality, this is all we have
plt.scatter(X[:, 0], X[:, 1])

## initialization
# randomly assing cluester centrs
cluster_centers = np.zeros((K, D))
for k in range(K):
    i = np.random.choice(N)
    cluster_centers[k] = X[i]

# k-means loop
max_iters = 20
cluster_identities = np.zeros(N)
saved_cluester_identities = []
# cost vars
min_dists = np.zeros(N)
costs = []
for i in range(max_iters):
    # check ofr convergence
    old_cluster_identities = cluster_identities.copy()
    saved_cluester_identities.append(old_cluster_identities)
    # step 1: determine cluster identities
    for n in range(N):
        closest_k = -1
        min_dist = float('inf')
        for k in range(K):
            d = (X[n] - cluster_centers[k]).dot(X[n] - cluster_centers[k])
            if d < min_dist:
                min_dist = d
                closest_k = k
            cluster_identities[n] = closest_k
        min_dists[n] = min_dist
    # store the cost
    costs.append(min_dists.sum())

    # step 2: recalculate means
    for k in range(K):
        cluster_centers[k, :] = X[cluster_identities == k].mean(axis=0)

    # step 2: check for convergence
    if np.all(old_cluster_identities == cluster_identities):
        print(f"Converged on step {i}")
        break

# plot cost per iteration
plt.clf()
plt.plot(costs)
plt.title("Cost per iteration")
plt.ylabel("Cost")
plt.xlabel("iteration")
plt.savefig("13/kmeans_cost")


# plot the means with the data
plt.clf()
plt.scatter(X[:, 0], X[:, 1], c=cluster_identities) # same as before
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], s=500, c='red', marker='*')
plt.savefig("13/kmeans_converged")

# show training progress
plt.clf()
M = len(saved_cluester_identities)
fig, ax = plt.subplots(figsize=(5, 5 * M))
for i in range(M):
    plt.subplot(M, 1, i+1)
    Y = saved_cluester_identities[i]
    plt.scatter(X[:, 0], X[:, 1], c=Y)

plt.savefig("13/kmeans_history")






