# Linear Classification Theory

* Recap of steps
    * Load in the data 
    * Instantiate the model
    * Train the model

* How is the model treinet?
    * cost function
    * gradient descent to minimize the cost

* Logistic Regression with > 2 inputs
    p(y = | x) = sig(w^T * x + b) = sig(SIG[D -> D=1]w_d * x_d + b)

* Tensorflow 2.0
    tf.keras.layers.Dense(output_size)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(D,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    => 1 is the output size, in this case 1 (binary classification)

    model.compile(optimizer='adam', 
                  loss='binary_crossentropy',
                  metrics=['accurary'])

    r = model.fit(X_train, y_train,
                  validation_data=(X_test, y_test),
                  epochs=100)
    
    plt.plot(r.history['loss'])