import subprocess
import zipfile
import numpy as np
import wget
import os
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt
from os.path import exists


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
    def load_image_into_numpy_array(image):
        # return np.array(Image.open(image))
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


