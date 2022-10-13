from __future__ import print_function, division

from Utils import Utils
import tensorflow as tf
from builtins import range, input

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten, Conv2D, BatchNormalization, ZeroPadding2D, \
    MaxPooling2D, Activation, add
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

from sklearn.metrics import confusion_matrix
import numpy as np
import os
import matplotlib.pyplot as plt

from glob import glob


def load_the_data(out_dir, train_path, valid_path, debug=False):
    out_dir += os.sep
    # useful for getting number of files
    image_files = glob(train_path + '/*/*.jp*g')
    valid_image_files = glob(valid_path + '/*/*.jp*g')
    # useful for getting number of classes
    folders = glob(train_path + '/*')
    # look at sn image for fun
    plt.clf()
    plt.imshow(image.load_img(np.random.choice(image_files)))
    plt.savefig(out_dir + "sample_blood_cell")
    if debug:
        plt.show()
    return image_files, valid_image_files, folders


def identity_block(input_, kernel_size, filters):
    f1, f2, f3 = filters

    # first convolution
    x = Conv2D(f1, (1, 1),
               # kernel_initializer='he_normal'
               )(input_)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # second convolution
    x = Conv2D(f2, kernel_size, padding='same',
               # kernel_initializer='he_normal'
               )(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # third convolution
    x = Conv2D(f3, (1, 1),
               # kernel_initializer='he_normal'
               )(x)
    x = BatchNormalization()(x)

    # Resnet bypass of the input layer
    x = add([x, input_])
    x = Activation('relu')(x)

    return x


def conv_block(input_,
               kernel_size,
               filters,
               strides=(2, 2)):
    f1, f2, f3 = filters

    x = Conv2D(f1, (1, 1), strides=strides,
               # kernel_initializer='he_normal'
               )(input_)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(f2, kernel_size, padding='same'
               # kernel_initializer = 'he_normal'
               )(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(f3, (1, 1),
               # kernel_initializer = 'he_normal')
               )(x)
    x = BatchNormalization()(x)

    shortcut = Conv2D(f3, (1, 1), strides,
                      # kernel_initializer = 'he_normal')
                      )(input_)
    shortcut = BatchNormalization()(shortcut)

    x = add([x, shortcut])
    x = Activation('relu')(x)

    return x


def preprocess_input2(x):
    x /= 127.5
    x -= 1.
    return x


def get_confusion_matrix(data_path, N, image_size, batch_size, image_generator, model):
    # we need to see the data in the same order
    # for both predictions and targets
    print("Generating confusion matrix", N)
    predictions = []
    targets = []
    i = 0
    for x, y in image_generator.flow_from_directory(data_path, target_size=image_size, shuffle=False,
                                                    batch_size=batch_size * 2):
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
    cm = confusion_matrix(targets, predictions)
    return cm


def build_the_model(out_dir,
                    image_size,
                    folders,
                    valid_path,
                    train_path,
                    batch_size,
                    epochs,
                    image_files,
                    valid_image_files):
    out_dir += os.sep
    # our custom resnet
    i = Input(shape=image_size + [3])
    x = ZeroPadding2D(padding=(3, 3))(i)
    x = Conv2D(64,
               (7, 7),
               strides=(2, 2),
               padding='valid',
               # kernel_initializer = 'he_normal'
               )(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = ZeroPadding2D(padding=(1, 1))(x)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)

    filters_1 = [64, 64, 256]
    filters_2 = [128, 128, 512]
    kernel_1 = 3

    x = conv_block(input_=x, kernel_size=kernel_1, filters=filters_1, strides=(1, 1))
    x = identity_block(input_=x, kernel_size=kernel_1, filters=filters_1)
    x = identity_block(input_=x, kernel_size=kernel_1, filters=filters_1)

    x = conv_block(input_=x, kernel_size=kernel_1, filters=filters_2, strides=(1, 1))
    x = identity_block(input_=x, kernel_size=kernel_1, filters=filters_2)
    x = identity_block(input_=x, kernel_size=kernel_1, filters=filters_2)
    x = identity_block(input_=x, kernel_size=kernel_1, filters=filters_2)

    # our layers - you can add more if you want
    x = Flatten()(x)
    # x = Dense(1000, activation='relu')(x)
    prediction = Dense(len(folders), activation='softmax')(x)

    # create a model object
    model = Model(inputs=i, outputs=prediction)

    # view the structure of the model
    model.summary()

    # tell the model what cost optimization method to use
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=Adam(learning_rate=0.0001),
        metrics=['accuracy']
    )

    return model


def train_the_model(model,
                    valid_path,
                    image_size,
                    out_dir,
                    batch_size,
                    epochs,
                    train_path,
                    image_files,
                    valid_image_files):
    # update dirs
    out_dir = out_dir + os.sep
    checkpoint_file = out_dir + os.sep + "checkpoint.chk"
    train_gen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        preprocessing_function=preprocess_input2
    )

    val_gen = ImageDataGenerator(
        preprocessing_function=preprocess_input2
    )

    # test generator to see how it works and some other usefull things
    test_gen = val_gen.flow_from_directory(valid_path, target_size=image_size, class_mode='sparse')
    print("test_ge.class_indices:", test_gen.class_indices)
    labels = [None] * len(test_gen.class_indices)
    for k, v in test_gen.class_indices.items():
        labels[v] = k

    # shoudl be not a strangely colored image
    for x, y in test_gen:
        print("min:", x[0].min(), ", max:", x[0].max())
        plt.clf()
        plt.title(labels[np.argmax(y[0])])
        plt.imshow(x[0])
        plt.savefig(out_dir + "sample_input_image")
        break

    # create generator
    train_generator = train_gen.flow_from_directory(
        train_path,
        target_size=image_size,
        shuffle=True,
        batch_size=batch_size,
        class_mode='sparse'
    )
    valid_generator = val_gen.flow_from_directory(
        valid_path,
        target_size=image_size,
        shuffle=True,
        batch_size=batch_size,
        class_mode='sparse'
    )

    # fit the model
    # tf.keras.callbacks.ModelCheckpoint
    # Callback to save the Keras model or model weights at some frequency.
    # ModelCheckpoint callback is used in conjunction with training using model.fit() to save a model or weights (in a checkpoint file) at some interval, so the model or weights can be loaded later to continue the training from the state saved.
    # A few options this callback provides include:
    # - Whether to only keep the model that has achieved the "best performance" so far, or whether to save the model at the end of every epoch regardless of performance.
    # - Definition of 'best'; which quantity to monitor and whether it should be maximized or minimized.
    # - The frequency it should save at. Currently, the callback supports saving at the end of every epoch, or after a fixed number of training batches.
    # - Whether only weights are saved, or the whole model is saved.
    r = model.fit(
        train_generator,
        validation_data=valid_generator,
        epochs=epochs,
        steps_per_epoch=len(image_files) // batch_size,
        validation_steps=len(valid_image_files) // batch_size,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='loss',
                patience=3,
                restore_best_weights=True,
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=checkpoint_file,
                save_weights_only=True,
                monitor='val_accuracy',
                mode='max',
                save_best_only=True
            ),
        ]
    )

    # loss
    plt.clf()
    plt.plot(r.histroy['loss'], label='train loss')
    plt.plot(r.history['val_loss'], label='val loss')
    plt.legend()
    plt.savefig(out_dir + "loss_per_iteration")

    # accuracies
    plt.clf()
    plt.plot(r.histroy['accuracy'], label='train acc')
    plt.plot(r.history['val_accuracy'], label='val acc')
    plt.legend()
    plt.savefig(out_dir + "accuracy_per_iteration")

    model.load_weights(checkpoint_file)

    return model, train_gen, val_gen, labels


def main():
    out_dir = "50"
    # re-size all the images to this
    image_size = [224, 224]  # feel free to change depending on dataset
    # training config
    epochs = 16
    # the number of samples to work through before updating the internal model parameters
    batch_size = 128
    #
    train_path = "blood_cell_images/TRAIN"
    valid_path = "blood_cell_images/TEST"
    debug = False
    image_files, valid_image_files, folders = load_the_data(out_dir, train_path=train_path, valid_path=valid_path)
    model = build_the_model(out_dir,
                            image_size,
                            folders,
                            valid_path,
                            train_path,
                            batch_size,
                            epochs,
                            image_files,
                            valid_image_files)
    model, train_gen, val_gen, labels = train_the_model(model,
                                                valid_path,
                                                image_size,
                                                out_dir,
                                                batch_size,
                                                epochs,
                                                train_path,
                                                image_files,
                                                valid_image_files)
    cm = get_confusion_matrix(data_path=train_path,
                              N=len(image_files),
                              image_size=image_size,
                              batch_size=batch_size,
                              image_generator=val_gen)
    valid_cm = get_confusion_matrix(data_path=valid_path,
                              N=len(valid_image_files),
                              image_size=image_size,
                              batch_size=batch_size,
                              image_generator=val_gen)

    Utils.plot_confusion_matrix(cm=cm, classes=labels, normalize=False, title="Confusion Matrix", cmap=plt.cm.Blues)
    # trace calc the sum of the diagonal
    train_accuracy = np.trace(cm) / cm.sum()
    val_accuracy = np.trace(valid_cm) / valid_cm.sum()
    print("train_accuracy:", train_accuracy)
    print("val_accuracy:", val_accuracy)



if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()
