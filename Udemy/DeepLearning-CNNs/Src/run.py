import os

scripts_list = ["13_classification.py",
                "15_regression.py",
                "29_ann_for_image_classification.py",
                "38_cnn_for_fashionmnist.py",
                "39_cnn_for_cifar.py",
                "42_improving_cifar10.py",
                "45_text_processing.py",
                "47_text_classification_cnn.py"]

for script in scripts_list:
    print("")
    print("######################################################################")
    print(f"# Executing script {script}")
    print("######################################################################")
    os.system(f"python {script}")
