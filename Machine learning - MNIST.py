



#one-hot encod
y_train = keras.utils.to_categorical(y_train, num_classes=10) #10 because 10 different numbers possible
y_verif = keras.utils.to_categorical(y_verif, num_classes=10)
y_test = keras.utils.to_categorical(y_test, num_classes=10)
print("\ntrain set :", X_train.shape, y_train.shape)
print("validation set :", X_verif.shape, y_verif.shape)
print("test set :", X_test.shape, y_test.shape, "\n")


model = keras.Sequential ((
    keras.layers.Dense(128, input_shape=(784,), activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(10, activation='softmax'), #proba
))


model.compile(
    optimizer='sgd', #opti  weight
    loss='categorical_crossentropy',
    metrics=['accuracy'] 
)
print("\ntraining session")
model.fit(X_train, y_train, epochs=5, validation_data=(X_verif, y_verif))

print("\ntest")
model.evaluate(X_test, y_test)