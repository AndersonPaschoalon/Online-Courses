import numpy as np
import sys

# using tf version 1
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def main():
    # matrix
    # Inserts a placeholder for a tensor that will be always fed.
    # This API is not compatible with eager execution and tf.function. To migrate to TF2, rewrite the code to be
    # compatible with eager execution. Check the migration guide on replacing Session.run calls. In TF2, you can just
    # pass tensors directly into ops and layers. If you want to explicitly set up your inputs, also see Keras
    # functional API on how to use tf.keras.Input to replace tf.compat.v1.placeholder. tf.function arguments also do
    # the job of tf.compat.v1.placeholder. For more details please read Better performance with tf.function.
    A = tf.placeholder(tf.float32, shape=(5, 5), name='A')
    # vector
    v = tf.placeholder(tf.float32)
    # multiplay matrix
    w = tf.matmul(A, v)

    # A class for running TensorFlow operations.
    # Session does not work with either eager execution or tf.function, and you should not invoke it directly.
    # To migrate code that uses sessions to TF2, rewrite the code without it. See the migration guide on replacing
    # Session.run calls.
    with tf.Session() as session:
        output = session.run(w, feed_dict={A: np.random.randn(5, 5), v: np.random.randn(5, 1)})
        print("output:", output, "\ntype:", type(output))

    shape = (2, 2)
    x = tf.Variable(tf.random_normal(shape))
    t = tf.Variable(0)
    init = tf.initialize_all_variables()

    with tf.Session() as session:
        out = session.run(init)
        print("out:", out)
        print("x.eval():", x.eval())
        print("t.eval():", t.eval())

    u = tf.Variable(20.0)
    cost = u*u + u + 1
    train_op = tf.train.GradientDescentOptimizer(0.3).minimize(cost)
    init = tf.initialize_all_variables()

    with tf.Session() as session:
        session.run(init)
        for i in range(12):
            session.run(train_op)
            print("i = %d, cost %.3f, u = %0.3f" % (i, cost.eval(), u.eval()))


if __name__ == '__main__':
    # print(tf.__version__)
    main()
