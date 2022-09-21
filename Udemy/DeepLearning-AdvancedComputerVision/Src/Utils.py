import subprocess

import numpy as np
import wget
import os
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt


class Utils:

    @staticmethod
    def wget_if_not_exit(url, output_file_path):
        if os.path.exists(output_file_path):
            print("File ", output_file_path, " already exist!")
        else:
            print("Downloading file ", output_file_path, " from url:" + url)
            wget.download(url, output_file_path)
            print("Download complete.")

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
