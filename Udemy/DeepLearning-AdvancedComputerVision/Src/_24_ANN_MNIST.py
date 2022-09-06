import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import itertools


def load_in_the_data():
    img_normalization = 255.0
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / img_normalization, x_test / img_normalization
    # This will print (60000, 28, 28)
    # x_train is a vector of 60k images of 28x28 pixels
    print("x_train.shape:", x_train.shape)
    print("x_test.shape:", x_test.shape)
    return x_train, y_train, x_test, y_test


# img_dimentions = (28, 28)
# n_neurons_l1 = 128
# activation_l1 = 'relu'
# dropout_percentage = 0.2
# n_neurons_output = 10
# activation_output = 'softmax'
# model_optimizer = 'adam
# cost_function = 'sparse_categorical_crossentropy'
# set_of_metrics = ['accuracy']
def build_the_model(img_dimentions,
                    n_neurons_l1,
                    activation_l1,
                    dropout_percentage,
                    n_neurons_output,
                    activation_output,
                    model_optimizer,
                    cost_function,
                    set_of_metrics):
    # create the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=img_dimentions),
        tf.keras.layers.Dense(n_neurons_l1, activation=activation_l1),
        tf.keras.layers.Dropout(dropout_percentage),
        tf.keras.layers.Dense(n_neurons_output, activation=activation_output)
    ])
    # Compile the model
    model.compile(optimizer=model_optimizer,
                  loss=cost_function,
                  metrics=set_of_metrics)

    return model


def train_the_model(model, x_train, y_train, x_test, y_test, n_epochs, output_dir):
    output_dir = output_dir + "\\"
    # Compile the model
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=n_epochs)
    # loss per iteration
    plt.clf()
    plt.plot(r.history['loss'], label='loss')
    plt.plot(r.history['val_loss'], label='val_loss')
    plt.legend()
    plt.savefig(output_dir + "loss_per_iteration")
    # plot accuracy per iteration
    plt.clf()
    plt.plot(r.history['accuracy'], label='acc')
    plt.plot(r.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.savefig(output_dir + "accuracy_per_iteration")


def evaluate_the_model(model, x_test, y_test, n_epochs, output_dir):
    print(model.evaluate(x_test, y_test))
    p_test = model.predict(x_test).argmax(axis=1)
    cm = confusion_matrix(y_test, p_test)
    plot_confusion_matrix(cm, list(range(n_epochs)), output_dir=output_dir)
    show_some_misclassified_examples(10, p_test, y_test, x_test, output_dir)

def plot_confusion_matrix(cm,
                          classes,
                          normalize=False,
                          title='Confusion Matrix',
                          cmap=plt.cm.Blues,
                          output_dir=""):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting 'normalize=True'
    """
    output_dir = output_dir + "\\"
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalizeed confusion matrix")
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
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    print("saving figure at ", output_dir + "confusion_matrix")
    plt.savefig(output_dir + "confusion_matrix")


def show_some_misclassified_examples(n_examples, p_test, y_test, x_test, out_dir):
    out_dir = out_dir + "\\"
    for j in range(n_examples):
        misclassified_idx = np.where(p_test != y_test)[0]
        i = np.random.choice(misclassified_idx)
        plt.clf()
        plt.imshow(x_test[i], cmap='gray')
        plt.title("True Label: %s, Predicted: %s" % (y_test[i], p_test[i]))
        file_name = out_dir + "misclassified_" + str(j)
        plt.savefig(file_name)


def main():
    #
    # Step 01 - Load in the data
    #
    x_train, y_train, x_test, y_test = load_in_the_data()

    #
    # Step 02 - Build the model
    #
    # size of the loaded image in pixels
    img_dimentions = (28, 28)
    # number of neurons in the first hidden layer
    n_neurons_l1 = 128
    # activation function for the first hidden layer, relu as usual
    activation_l1 = 'relu'
    # random neurons will be turned off, so the training process will not be so dependent of few neurons
    dropout_percentage = 0.2
    # number of neurons in the output, the number of classes of the output
    n_neurons_output = 10
    # output function to give a 0-1 probability for each neuron in the output
    activation_output = 'softmax'
    model_optimizer = 'adam'
    cost_function = 'sparse_categorical_crossentropy'
    set_of_metrics = ['accuracy']
    model = build_the_model(img_dimentions,
                            n_neurons_l1,
                            activation_l1,
                            dropout_percentage,
                            n_neurons_output,
                            activation_output,
                            model_optimizer,
                            cost_function,
                            set_of_metrics)

    #
    # Step 03 - Train the model
    #
    n_epochs = 20
    output_dir = "24"
    train_the_model(model, x_train, y_train, x_test, y_test, n_epochs, output_dir)

    # Step 04 - Evaluate the model
    evaluate_the_model(model, x_test, y_test, n_epochs, output_dir)

    # Step 05 - Make Predictions


if __name__ == '__main__':
    print("TensorFlow version:", tf.__version__)
    main()
