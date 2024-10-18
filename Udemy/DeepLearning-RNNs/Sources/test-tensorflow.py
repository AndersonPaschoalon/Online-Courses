import tensorflow as tf
import numpy as np

# Print TensorFlow version
print(f"TensorFlow version: {tf.__version__}")

# Define a simple neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(5,)),  # Input layer with 5 features
    tf.keras.layers.Dense(1, activation='linear')  # Output layer with 1 neuron
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Create some dummy data for testing
x_train = np.random.rand(100, 5)  # 100 samples, each with 5 features
y_train = np.random.rand(100, 1)  # 100 target values

# Train the model
model.fit(x_train, y_train, epochs=5)

# Test the model with new data
x_test = np.random.rand(10, 5)  # 10 new samples
predictions = model.predict(x_test)

print("Predictions on test data:")
print(predictions)

# Perform some other calculations
a = tf.constant([2.0, 3.0])
b = tf.constant([4.0, 5.0])
c = a + b

print("Result of a + b:")
print(c.numpy())

d = tf.reduce_sum(a * b)

print("Result of sum(a * b):")
print(d.numpy())
