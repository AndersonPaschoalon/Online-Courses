import subprocess
import wget
import os

class Utils:

    @staticmethod
    def wget_if_not_exit(url, output_file_path):
        if os.path.exists(output_file_path):
            print("File ", output_file_path, " already exist!")
        else:
            print("Downloading file ", output_file_path, " from url:" + url)
            wget.download(url, output_file_path)
            print("Download complete.")