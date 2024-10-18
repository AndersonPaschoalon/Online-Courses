import tensorflow as tf

print(tf.__version__)


from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

data = load_breast_cancer()

print("data.keys():", data.keys())
# data.data.shape: (569, 30) - (number of samples, number of features)
print("data.data.shape:", data.data.shape)

X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.33)
N, D = X_train.shape
print(f"(N, D) = ({N}, {D})")

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(D,)),
    tf.keras.layers.Dense(1, activation = 'sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
r = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100)

print("Train score:", model.evaluate(X_train, y_train))
print("Test score:", model.evaluate(X_test, y_test))


import matplotlib.pyplot as plt
import os 

out_dir = os.path.join("Results", "12")

plt.clf()
plt.plot(r.history['loss'], label='loss')
plt.legend()
plt.savefig(os.path.join(out_dir, "loss"))

plt.clf()
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()
plt.savefig(os.path.join(out_dir, "val_loss"))
# do the plot

plt.clf()
plt.plot(r.history['accuracy'], label='accuracy')
plt.legend()
plt.savefig(os.path.join(out_dir, "accuracy"))

plt.clf()
plt.plot(r.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.savefig(os.path.join(out_dir, "val_accuracy"))






















#