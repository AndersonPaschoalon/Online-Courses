# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2.md
# https://lazyprogrammer.me/course_files/object_detection_images/walkingdog.jpeg
# https://lazyprogrammer.me/course_files/object_detection_images/traffic.jpeg
# https://lazyprogrammer.me/course_files/object_detection_images/jungle.jpeg
# https://lazyprogrammer.me/course_files/object_detection_images/intersection.jpeg
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md
# https://github.com/tensorflow/models/blob/master/research/object_detection/data/mscoco_label_map.pbtxt


import os
import pathlib
import tensorflow as tf

import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from Utils import Utils


def load_image_into_numpy_array(path):
    return np.array(Image.open(path))


def prepare_enviroment():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    # Download these files and save in the 61 folder
    # https://lazyprogrammer.me/course_files/object_detection_images/walkingdog.jpeg
    # https://lazyprogrammer.me/course_files/object_detection_images/traffic.jpeg
    # https://lazyprogrammer.me/course_files/object_detection_images/jungle.jpeg
    # https://lazyprogrammer.me/course_files/object_detection_images/intersection.jpeg
    image_paths = ['61/intersection.jpeg', '61/traffic.jpeg', '61/jungle.jpeg', '61/walkingdog.jpeg']
    return image_paths


def download_the_model():
    curr_path = Utils.pwd()
    # donwload and extract models files
    # get Utls form the "object detection zoo"
    # https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md
    url = 'http://download.tensorflow.org/models/object_detection/ssd_resnet101_v1_fpn_shared_box_predictor_oid_512x512_sync_2019_01_20.tar.gz'
    path_fname_model = os.path.join(curr_path, '61', 'ssd_resnet101_model')
    print("path_fname_model:", path_fname_model)
    path_to_model_dir = tf.keras.utils.get_file(fname=path_fname_model,  # pode ser setado para qualquer coisa
                                                origin=url,
                                                untar=True)
    print("path_to_model_dir:", path_to_model_dir)

    url_labels = "https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt"
    path_fname_labels = os.path.join(curr_path, '61', "mscoco_label_map.pbtxt")
    print("path_fname_labels:", path_fname_labels)
    path_to_labels = tf.keras.utils.get_file(fname=path_fname_labels,
                                             origin=url_labels,
                                             untar=False)

    return path_to_model_dir, path_to_labels


def load_in_the_model(path_to_model_dir, path_to_labels):
    # Indexes
    HELP="""
    For this line tu run, I had to replace this line 
      #with tf.gfile.GFile(path, 'r') as fid:
    By this:
        with tf.io.gfile.GFile(path, 'r') as fid:
    In the library source code, in the file:
        label_map_util.py
    """
    print("Loading Category Index from {}...".format(path_to_labels))
    category_index = label_map_util.create_category_index_from_labelmap(path_to_labels,
                                                                        use_display_name=True)
    print(category_index)

    # Model
    path_to_model = os.path.join(path_to_model_dir, 'saved_model')
    print("Loading model...")
    start_time = time.time()

    # Load saved model and build detection function
    detect_fn = tf.saved_model.load(path_to_model)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds to load the model.'.format(elapsed_time))

    return detect_fn, category_index


def detect_objects(image_path, detect_fn, category_index):
    print('Running inference for {}...'.format(image_path))
    image_np = load_image_into_numpy_array(image_path)

    # The input needs to be a tensor, convert it using tf.convert_to_tensor
    input_tensor = tf.convert_to_tensor(image_np)

    # The model expects a batch of images, so add an axis with tf.newaxis
    input_tensor = input_tensor[tf.newaxis, ...]

    # Do the detection
    # detections = detect_fn(input_tensor)
    detections = detect_fn.signatures['serving_default'](input_tensor)

    # all outputs are batches tensors
    # convert the numpy arrays, and take index [0], to remove the batch dimension.
    # We're only interested in hte first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    # Show classes
    # unique_classes = set(detections['detection_classes'])
    # print("Classes found:")
    # for c in unique_classes:
    #     print(category_index[c]['name'])

    image_np_with_detection = image_np.copy()
    viz_utils.visualize_boxes_and_labels_on_image_array(image_np_with_detection,
                                                        detections['detection_boxes'],
                                                        detections['detection_classes'],
                                                        detections['detection_scores'],
                                                        category_index=category_index,
                                                        use_normalized_coordinates=True,
                                                        max_boxes_to_draw=200,
                                                        min_score_thresh=0.30,
                                                        agnostic_mode=False)
    plt.clf()
    plt.figure(figsize=(15, 10))
    plt.imshow(image_np_with_detection)
    print("Done")
    #plt.show()
    plt.savefig(image_path + ".detection.jpg")


def main():
    image_paths = prepare_enviroment()
    path_to_model_dir, path_to_labels = download_the_model()
    detect_fn, category_index = load_in_the_model(path_to_model_dir, path_to_labels)
    detect_objects(image_paths[0], detect_fn, category_index)
    detect_objects(image_paths[1], detect_fn, category_index)
    detect_objects(image_paths[2], detect_fn, category_index)
    detect_objects(image_paths[3], detect_fn, category_index)

if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()