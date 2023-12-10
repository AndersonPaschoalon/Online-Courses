from keras.backend import learning_phase

import util
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

params = {
    "learning_rate": 0.001,
    "epochs": 50,
    "batch_size": 64,
    "out_dir": ".\\Results\\11"
}

class Autoencoder:

    def __init__(self, D, M, learning_rate=0.001):
        tf.compat.v1.disable_eager_execution()

        # represents a batch of training data
        self.X = tf.compat.v1.placeholder(tf.compat.v1.float32, shape=(None, D))

        # input -> hidden layer
        # self.W = tf.compat.v1.Variable(tf.compat.v1.random_normal(shape=(D, M) * int(2 / np.sqrt(M))))
        self.W = tf.compat.v1.Variable(tf.compat.v1.random_normal(shape=(D, M)))
        self.b = tf.compat.v1.Variable(np.zeros(M).astype(np.float32))

        # hodden -> output layer
        # self.V = tf.compat.v1.Variable(tf.compat.v1.random_normal(shape=(M, D) * int(2 / np.sqrt(D))))
        self.V = tf.compat.v1.Variable(tf.compat.v1.random_normal(shape=(M, D)))
        self.c = tf.compat.v1.Variable(np.zeros(D).astype(np.float32))

        # construct the reconstruction
        self.Z = tf.compat.v1.nn.relu(tf.matmul(self.X, self.W) + self.b)
        logists = tf.compat.v1.matmul(self.Z, self.V) + self.c
        self.X_hat = tf.compat.v1.nn.sigmoid(logists)

        # compute the cost
        self.cost = tf.compat.v1.reduce_sum(
            tf.compat.v1.nn.sigmoid_cross_entropy_with_logits(
                labels=self.X,
                logits=logists
            )
        )

        # make the trainer
        self.train_op = tf.compat.v1.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(self.cost)

        # set up session and variables for later
        self.init_op = tf.compat.v1.global_variables_initializer()
        self.sess = tf.compat.v1.InteractiveSession()
        self.sess.run(self.init_op)

    def fit(self, X, epochs=30, batch_sz=64, out_dir=""):
        costs = []
        n_batches = len(X) // batch_sz
        print(f"n_batches:{n_batches}")
        for i in range(epochs):
            print(f"epoch:{i}")
            np.random.shuffle(X)
            for j in range(n_batches):
                batch = X[j*batch_sz:(j+1)*batch_sz]
                _, c, = self.sess.run((self.train_op, self.cost), feed_dict={self.X: batch})
                c /= batch_sz
                costs.append(c)
                if j % 100 == 0:
                    print("iter:%d, cost: %.3f" % (j, c))
        plt.plot(costs)
        plt.savefig(os.path.join(out_dir, "costs"))

    def predict(self, X):
        return self.sess.run(self.X_hat, feed_dict={self.X: X})


def main(params):
    ret, X, Y = util.get_mnist()
    if not ret:
        print("Error @util.get_mnist() ")
        return
    model = Autoencoder(D=784, M=300, learning_rate=params["learning_rate"])
    model.fit(X, epochs=params["epochs"], batch_sz=params["batch_size"], out_dir=params["out_dir"])

    done = False
    count_gens_max = 5
    count_gens = 0
    while not done:
        i = np.random.choice(len(X))
        x = X[i]
        im = model.predict([x]).reshape(28, 28)
        plt.subplot(1, 2, 1)
        plt.imshow(x.reshape(28, 28), cmap='gray')
        plt.title("Original")
        plt.subplot(1, 2, 2)
        plt.imshow(im, cmap='gray')
        plt.title("Reconstruction")
        # plt.show()
        fig_name = os.path.join(params["out_dir"], f"Original_vs_Reconstructed_{count_gens}")

        # ans = input("Generate another?")
        # if ans and ans[0] in ('n' or 'N'):
        #     done = True
        count_gens += 1
        if count_gens >= count_gens_max:
            done = True


if __name__ == '__main__':
    main(params)



