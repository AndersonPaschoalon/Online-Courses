import os

scripts_list = ["_06_SamplingDemo_BayesClassifier.py",
                "_08_SamplingDemo_BayesClassifierWithGMM.py",
                "_11_Autoencoder_tf.py", ]

for script in scripts_list:
    print("")
    print("######################################################################")
    print(f"# Executing script {script}")
    print("######################################################################")
    os.system(f"python {script}")
