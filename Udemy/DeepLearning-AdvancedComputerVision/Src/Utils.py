from __future__ import print_function, division
from builtins import range

import subprocess
import zipfile
import numpy as np
import wget
import os
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt
from os.path import exists
# from numba import cuda

# Note: you may need to update your version of future
# sudo pip install -U future
# Some utility functions we need for the class.
# For the class Data Science: Practical Deep Learning Concepts in Theano and TensorFlow
# https://deeplearningcourses.com/c/data-science-deep-learning-in-theano-tensorflow
# https://www.udemy.com/data-science-deep-learning-in-theano-tensorflow
# Note: run this from the current folder it is in.
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression


class Utils:

    @staticmethod
    def wget_if_not_exit(url, output_file_path):
        if os.path.exists(output_file_path):
            print("File ", output_file_path, " already exist!")
        else:
            print("Downloading file ", output_file_path, " from url:" + url)
            wget.download(url, out=output_file_path)
            print("Download complete.")

    @staticmethod
    def unzip(zip_file, dst_dir = ""):
        if not os.path.exists(zip_file):
            print("Error: ZIP file ", zip_file, " does not exist!")
            return False
        zip_no_ext = os.path.basename(os.path.splitext(zip_file)[0])
        if dst_dir == "":
            dst_dir = zip_no_ext
        with zipfile.ZipFile(zip_no_ext, 'r') as zip_ref:
            zip_ref.extractall(dst_dir)
        return True

    @staticmethod
    def plot_confusion_matrix(cm,
                              classes,
                              normalize=False,
                              title='Confusion Matrix',
                              cmap=plt.cm.Blues,
                              out_file_name="confusion_matrix"):
        """
        This function prints and plots the confision matrix
        """
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print("Confusion matrix, without normalization")

        print(cm)

        plt.clf()
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment='center',
                     color='white' if cm[i, j] > thresh else 'black')
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(out_file_name)


    @staticmethod
    def mkdir(p):
        if not os.path.exists(p):
            os.mkdir(p)

    @staticmethod
    def link(src, dst):
        if not os.path.exists(dst):
            os.symlink(src, dst, target_is_directory=True)

    @staticmethod
    def make_limited_datasets_fruits():
        path_to_create = '.\\fruits-360_dataset\\fruits-360-small'
        if os.path.exists(path_to_create):
            return True
        else:
            try:
                Utils.mkdir(path_to_create)
                classes = [
                    'Apple Golden 1',
                    'Avocado',
                    'Lemon',
                    'Mango',
                    'Kiwi',
                    'Banana',
                    'Strawberry',
                    'Raspberry'
                ]
                train_path_from = os.path.abspath('./fruits-360_dataset/fruits-360/Training')
                valid_path_from = os.path.abspath('./fruits-360_dataset/fruits-360/Test')
                train_path_to = os.path.abspath('./fruits-360_dataset/fruits-360-small/Training')
                valid_path_to = os.path.abspath('./fruits-360_dataset/fruits-360-small/Validation')
                Utils.mkdir(train_path_to)
                Utils.mkdir(valid_path_to)

                for c in classes:
                    Utils.link(train_path_from + '/' + c, train_path_to + '/' + c)
                    Utils.link(valid_path_from + '/' + c, valid_path_to + '/' + c)
            except:
                error_msg = """
                Error  loading the dataset!
                Before executing this command you must:
                1. Download the fruits dataset from here: https://www.kaggle.com/datasets/moltean/fruits
                2. Place the fruits-360_dataset folder in the same directory of this code:
                   \Src\ 
                       |__ Utils.py
                       |__ fruits-3060_dataset/ 
                3. The folder structure of fruits-3060_dataset must be:
                    fruits-3060_dataset\
                    |__ fruits-360\
                        |__ Training\*\*.jpg
                        |__ Validation\*\*.jpg
                    |__ fruits-360-small\
                        |__ Training\*\*.jpg
                        |__ Validation\*\*.jpg
                """
                print(error_msg)

    @staticmethod
    def pwd():
        curr_dir = os.path.abspath(os.getcwd())
        print(curr_dir)
        return curr_dir

    # convert image -> numpy array
    @staticmethod
    def load_image_into_numpy_array(image):
        # return np.array(Image.open(image))
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

    @staticmethod
    def file_name(file_path):
        return os.path.basename(os.path.splitext(file_path)[0])

    @staticmethod
    def reset_gpu():
        print("todo")
        #device = cuda.get_current_device()
        #device.reset()

    ####################################################################################################################
    # Utils functions from Apendix
    ####################################################################################################################

    @staticmethod
    def get_clouds():
        Nclass = 500
        D = 2

        X1 = np.random.randn(Nclass, D) + np.array([0, -2])
        X2 = np.random.randn(Nclass, D) + np.array([2, 2])
        X3 = np.random.randn(Nclass, D) + np.array([-2, 2])
        X = np.vstack([X1, X2, X3])

        Y = np.array([0] * Nclass + [1] * Nclass + [2] * Nclass)
        return X, Y

    @staticmethod
    def get_spiral():
        # Idea: radius -> low...high
        #           (don't start at 0, otherwise points will be "mushed" at origin)
        #       angle = low...high proportional to radius
        #               [0, 2pi/6, 4pi/6, ..., 10pi/6] --> [pi/2, pi/3 + pi/2, ..., ]
        # x = rcos(theta), y = rsin(theta) as usual

        radius = np.linspace(1, 10, 100)
        thetas = np.empty((6, 100))
        for i in range(6):
            start_angle = np.pi * i / 3.0
            end_angle = start_angle + np.pi / 2
            points = np.linspace(start_angle, end_angle, 100)
            thetas[i] = points

        # convert into cartesian coordinates
        x1 = np.empty((6, 100))
        x2 = np.empty((6, 100))
        for i in range(6):
            x1[i] = radius * np.cos(thetas[i])
            x2[i] = radius * np.sin(thetas[i])

        # inputs
        X = np.empty((600, 2))
        X[:, 0] = x1.flatten()
        X[:, 1] = x2.flatten()

        # add noise
        X += np.random.randn(600, 2) * 0.5

        # targets
        Y = np.array([0] * 100 + [1] * 100 + [0] * 100 + [1] * 100 + [0] * 100 + [1] * 100)
        return X, Y

    @staticmethod
    def get_transformed_data():
        print("Reading in and transforming data...")

        if not os.path.exists('../large_files/train.csv'):
            print('Looking for ../large_files/train.csv')
            print('You have not downloaded the data and/or not placed the files in the correct location.')
            print('Please get the data from: https://www.kaggle.com/c/digit-recognizer')
            print('Place train.csv in the folder large_files adjacent to the class folder')
            exit()

        df = pd.read_csv('../large_files/train.csv')
        data = df.values.astype(np.float32)
        np.random.shuffle(data)

        X = data[:, 1:]
        Y = data[:, 0].astype(np.int32)

        Xtrain = X[:-1000]
        Ytrain = Y[:-1000]
        Xtest = X[-1000:]
        Ytest = Y[-1000:]

        # center the data
        mu = Xtrain.mean(axis=0)
        Xtrain = Xtrain - mu
        Xtest = Xtest - mu

        # transform the data
        pca = PCA()
        Ztrain = pca.fit_transform(Xtrain)
        Ztest = pca.transform(Xtest)

        Utils.plot_cumulative_variance(pca)

        # take first 300 cols of Z
        Ztrain = Ztrain[:, :300]
        Ztest = Ztest[:, :300]

        # normalize Z
        mu = Ztrain.mean(axis=0)
        std = Ztrain.std(axis=0)
        Ztrain = (Ztrain - mu) / std
        Ztest = (Ztest - mu) / std

        return Ztrain, Ztest, Ytrain, Ytest

    @staticmethod
    def get_normalized_data():
        print("Reading in and transforming data...")

        if not os.path.exists('../large_files/train.csv'):
            print('Looking for ../large_files/train.csv')
            print('You have not downloaded the data and/or not placed the files in the correct location.')
            print('Please get the data from: https://www.kaggle.com/c/digit-recognizer')
            print('Place train.csv in the folder large_files adjacent to the class folder')
            exit()

        df = pd.read_csv('../large_files/train.csv')
        data = df.values.astype(np.float32)
        np.random.shuffle(data)
        X = data[:, 1:]
        Y = data[:, 0]

        Xtrain = X[:-1000]
        Ytrain = Y[:-1000]
        Xtest = X[-1000:]
        Ytest = Y[-1000:]

        # normalize the data
        mu = Xtrain.mean(axis=0)
        std = Xtrain.std(axis=0)
        np.place(std, std == 0, 1)
        Xtrain = (Xtrain - mu) / std
        Xtest = (Xtest - mu) / std

        return Xtrain, Xtest, Ytrain, Ytest

    @staticmethod
    def plot_cumulative_variance(pca):
        P = []
        for p in pca.explained_variance_ratio_:
            if len(P) == 0:
                P.append(p)
            else:
                P.append(p + P[-1])
        plt.plot(P)
        plt.show()
        return P

    @staticmethod
    def forward(X, W, b):
        # softmax
        a = X.dot(W) + b
        expa = np.exp(a)
        y = expa / expa.sum(axis=1, keepdims=True)
        return y

    @staticmethod
    def predict(p_y):
        return np.argmax(p_y, axis=1)

    @staticmethod
    def error_rate(p_y, t):
        prediction = Utils.predict(p_y)
        return np.mean(prediction != t)


    def cost(p_y, t):
        tot = t * np.log(p_y)
        return -tot.sum()

    @staticmethod
    def gradW(t, y, X):
        return X.T.dot(t - y)

    @staticmethod
    def gradb(t, y):
        return (t - y).sum(axis=0)

    @staticmethod
    def y2indicator(y):
        N = len(y)
        y = y.astype(np.int32)
        ind = np.zeros((N, 10))
        for i in range(N):
            ind[i, y[i]] = 1
        return ind

    @staticmethod
    def benchmark_full():
        Xtrain, Xtest, Ytrain, Ytest = Utils.get_normalized_data()

        print("Performing logistic regression...")
        # lr = LogisticRegression(solver='lbfgs')

        # convert Ytrain and Ytest to (N x K) matrices of indicator variables
        N, D = Xtrain.shape
        Ytrain_ind = Utils.y2indicator(Ytrain)
        Ytest_ind = Utils.y2indicator(Ytest)

        W = np.random.randn(D, 10) / np.sqrt(D)
        b = np.zeros(10)
        LL = []
        LLtest = []
        CRtest = []

        # reg = 1
        # learning rate 0.0001 is too high, 0.00005 is also too high
        # 0.00003 / 2000 iterations => 0.363 error, -7630 cost
        # 0.00004 / 1000 iterations => 0.295 error, -7902 cost
        # 0.00004 / 2000 iterations => 0.321 error, -7528 cost

        # reg = 0.1, still around 0.31 error
        # reg = 0.01, still around 0.31 error
        lr = 0.00004
        reg = 0.01
        for i in range(500):
            p_y = Utils.forward(Xtrain, W, b)
            # print "p_y:", p_y
            ll = Utils.cost(p_y, Ytrain_ind)
            LL.append(ll)

            p_y_test = Utils.forward(Xtest, W, b)
            lltest = Utils.cost(p_y_test, Ytest_ind)
            LLtest.append(lltest)

            err = Utils.error_rate(p_y_test, Ytest)
            CRtest.append(err)

            W += lr * (Utils.gradW(Ytrain_ind, p_y, Xtrain) - reg * W)
            b += lr * (Utils.gradb(Ytrain_ind, p_y) - reg * b)
            if i % 10 == 0:
                print("Cost at iteration %d: %.6f" % (i, ll))
                print("Error rate:", err)

        p_y = Utils.forward(Xtest, W, b)
        print("Final error rate:", Utils.error_rate(p_y, Ytest))
        iters = range(len(LL))
        plt.plot(iters, LL, iters, LLtest)
        plt.show()
        plt.plot(CRtest)
        plt.show()

    @staticmethod
    def benchmark_pca():
        Xtrain, Xtest, Ytrain, Ytest = Utils.get_transformed_data()
        print("Performing logistic regression...")

        N, D = Xtrain.shape
        Ytrain_ind = np.zeros((N, 10))
        for i in range(N):
            Ytrain_ind[i, Ytrain[i]] = 1

        Ntest = len(Ytest)
        Ytest_ind = np.zeros((Ntest, 10))
        for i in range(Ntest):
            Ytest_ind[i, Ytest[i]] = 1

        W = np.random.randn(D, 10) / np.sqrt(D)
        b = np.zeros(10)
        LL = []
        LLtest = []
        CRtest = []

        # D = 300 -> error = 0.07
        lr = 0.0001
        reg = 0.01
        for i in range(200):
            p_y = Utils.forward(Xtrain, W, b)
            # print "p_y:", p_y
            ll = Utils.cost(p_y, Ytrain_ind)
            LL.append(ll)

            p_y_test = Utils.forward(Xtest, W, b)
            lltest = Utils.cost(p_y_test, Ytest_ind)
            LLtest.append(lltest)

            err = Utils.error_rate(p_y_test, Ytest)
            CRtest.append(err)

            W += lr * (Utils.gradW(Ytrain_ind, p_y, Xtrain) - reg * W)
            b += lr * (Utils.gradb(Ytrain_ind, p_y) - reg * b)
            if i % 10 == 0:
                print("Cost at iteration %d: %.6f" % (i, ll))
                print("Error rate:", err)

        p_y = Utils.forward(Xtest, W, b)
        print("Final error rate:", Utils.error_rate(p_y, Ytest))
        iters = range(len(LL))
        plt.plot(iters, LL, iters, LLtest)
        plt.show()
        plt.plot(CRtest)
        plt.show()

