from __future__ import print_function, division

from Utils import Utils
import tensorflow as tf
from builtins import range, input

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

from glob import glob
from Utils import Utils


def load_the_data(IMAGE_SIZE, out_dir, debug=True):
    out_dir += "\\"
    Utils.make_limited_datasets_fruits()
    # re-size all the images to this
    # IMAGE_SIZE = [100, 100] # fell free to change depending on the dataset
    # train_path = "fruits-360_dataset/fruits-360/Training"
    # valid_path = "fruits-360_dataset/fruits-360/Test"
    train_path = "fruits-360_dataset/fruits-360-small/Training"
    valid_path = "fruits-360_dataset/fruits-360-small/Validation"
    # useful for getting number of files
    image_files = glob(train_path + '/*/*.jp*g')
    valid_image_files = glob(valid_path + '/*/*.jp*g')

    # useful for getting number of classes
    folders = glob(train_path + '/*')

    if debug:
        print("image_files: ", image_files)
        print("valid_image_files: ", valid_image_files)
        print("folders: ", folders)

    plt.clf()
    plt.imshow(image.img_to_array(image.load_img(np.random.choice(image_files))).astype('uint8'))
    plt.savefig(out_dir + "random_fruit")

    return image_files, valid_image_files, folders, valid_path, train_path


def build_the_model(IMAGE_SIZE, folders):
    # add a preprocessing layer to the front of VGG
    vgg = VGG16(input_shape=IMAGE_SIZE + [3],
                weights='imagenet',  # wich pre-trained wheits we want
                include_top=False)  # we want everything, except the laast layer

    # dont train existing weights
    for layer in vgg.layers:
        layer.trainable = False

    # out layers = you can add more if you want
    x = Flatten()(vgg.output)
    # x = Dense(1000, activation='relu')(x)
    prediction = Dense(len(folders), activation='softmax')(x)

    # create the model object
    model = Model(inputs=vgg.input, outputs=prediction)

    # view the structure of the model
    model.summary()

    # tell the model waht cost and optimization method to use
    model.compile(
        loss='categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )

    return model


def create_and_test_an_image_data_generator(out_dir, valid_path, IMAGE_SIZE):
    out_dir += "\\"
    # create an instance of ImageDataGenerator
    gen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        preprocessing_function=preprocess_input  # required parameter to pass the images to VGG (reorder the channels)
    )

    # test generator to see how it works and some other useful things

    # get label mapping for confusion matrix plot later
    print("-- gen.flow_from_directory")
    # search for images in folders, each folder is a class
    test_gen = gen.flow_from_directory(valid_path, target_size=IMAGE_SIZE)
    print("-- test_gen.class_indices:", test_gen.class_indices)
    labels = [None] * len(test_gen.class_indices)
    for k, v in test_gen.class_indices.items():
        labels[v] = k

    # should be a strangely colored image (due to VGG weights being BGR)
    for x, y in test_gen:
        print("min:", x[0].min(), ", max:", x[0].max())
        plt.clf()
        plt.title(labels[np.argmax(y[0])])
        plt.imshow(x[0])
        plt.savefig(out_dir + "image_data_generator_test")
        break

    return gen, labels


def create_generators(gen, train_path, valid_path, IMAGE_SIZE, batch_size):
    train_generator = gen.flow_from_directory(
        train_path,
        target_size=IMAGE_SIZE,
        shuffle=True,
        batch_size=batch_size,
    )
    valid_generator = gen.flow_from_directory(
        valid_path,
        target_size=IMAGE_SIZE,
        shuffle=True,
        batch_size=batch_size,
    )
    return train_generator, valid_generator


def fit_the_model(model, train_generator, valid_generator, epochs, image_files, valid_image_files, batch_size):
    r = model.fit(
        train_generator,
        validation_data=valid_generator,
        epochs=epochs,
        steps_per_epoch=len(image_files) // batch_size,
        validation_steps=len(valid_image_files) // batch_size,
    )
    return r, model


def get_confusion_matrix(model, gen, IMAGE_SIZE, batch_size, data_path, N):
    # we need to see the data in the same order
    # for both predictions and targets
    print("Generating confusion matrix", N)
    predictions = []
    targets = []
    i = 0
    for x, y in gen.flow_from_directory(data_path, target_size=IMAGE_SIZE, shuffle=False, batch_size=batch_size * 2):
        i += 1
        if i % 50 == 0:
            print(i)
        p = model.predict(x)
        p = np.argmax(p, axis=1)
        y = np.argmax(y, axis=1)
        predictions = np.concatenate((predictions, p))
        targets = np.concatenate((targets, y))
        if len(targets) >= N:
            break
    # endfor
    cm = confusion_matrix(targets, predictions)
    return cm


def plot_confusion_matrix(out_dir, r, model, gen, IMAGE_SIZE, batch_size, train_path, valid_path, image_files,
                          valid_image_files, labels):
    out_dir += "\\"
    cm = get_confusion_matrix(model, gen, IMAGE_SIZE, batch_size, train_path, len(image_files))
    print(cm)
    valid_cm = get_confusion_matrix(model, gen, IMAGE_SIZE, batch_size, valid_path, len(valid_image_files))
    print(valid_cm)

    # plot some data

    # loss
    plt.clf()
    plt.plot(r.history['loss'], label='train loss')
    plt.plot(r.history['val_loss'], label='val loss')
    plt.legend()
    plt.savefig(out_dir + "model_loss")
    # plt.show()
    # accuracies
    plt.clf()
    plt.plot(r.history['accuracy'], label='train acc')
    plt.plot(r.history['val_accuracy'], label='val acc')
    plt.legend()
    plt.savefig(out_dir + "model_accuracy")
    # plt.show()

    Utils.plot_confusion_matrix(cm=cm,
                                classes=labels,
                                normalize=False,
                                title='Confusion Matrix',
                                cmap=plt.cm.Blues,
                                out_file_name=out_dir + "//" + "confusion_matrix")
    Utils.plot_confusion_matrix(cm=valid_cm,
                                classes=labels,
                                normalize=False,
                                title='Validation confusion matrix',
                                cmap=plt.cm.Blues,
                                out_file_name=out_dir + "//" + "Validation_confusion_matrix")


def main():
    out_dir = "42"
    epochs = 5
    #epochs = 5
    batch_size = 32
    image_size = [100, 100]
    image_files, valid_image_files, folders, valid_path, train_path = load_the_data(image_size,
                                                                                    out_dir,
                                                                                    debug=False)
    model = build_the_model(image_size, folders)
    gen, labels = create_and_test_an_image_data_generator(out_dir, valid_path, image_size)
    train_generator, valid_generator = create_generators(gen, train_path, valid_path, image_size, batch_size)
    r, model = fit_the_model(model,
                             train_generator,
                             valid_generator,
                             epochs,
                             image_files,
                             valid_image_files,
                             batch_size)
    plot_confusion_matrix(out_dir,
                          r,
                          model,
                          gen,
                          image_size,
                          batch_size,
                          train_path,
                          valid_path,
                          image_files,
                          valid_image_files,
                          labels)


if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()
