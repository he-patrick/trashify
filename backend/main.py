import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.models import model_from_json

size = 100

# paper plastic glass aluminum
data = []
labels = []

# creating dataset for crumpled paper images
crumpled_papers = os.listdir("ML-trash-images/paper/crumpled_paper")
for paper in crumpled_papers:
    imag = cv2.imread("ML-trash-images/paper/crumpled_paper/"+paper)
    img_from_ar = Image.fromarray(imag, 'RGB')
    resized_image = img_from_ar.resize((size, size))
    data.append(np.array(resized_image))
    labels.append(0)

# creating dataset for paper cardboard images
cardboards = os.listdir("ML-trash-images/paper/cardboard")
for cardboard in cardboards:
    imag = cv2.imread("ML-trash-images/paper/cardboard/"+cardboard)
    img_from_ar = Image.fromarray(imag, 'RGB')
    resized_image = img_from_ar.resize((size, size))
    data.append(np.array(resized_image))
    labels.append(1)

# creating dataset for aluminum cans images
cans = os.listdir("ML-trash-images/aluminum/cans")
for can in cans:
    imag = cv2.imread("ML-trash-images/aluminum/cans/"+can)
    img_from_ar = Image.fromarray(imag, 'RGB')
    resized_image = img_from_ar.resize((size, size))
    data.append(np.array(resized_image))
    labels.append(2)

# creating dataset for aluminum lids images
lids = os.listdir("ML-trash-images/aluminum/lids")
for lid in lids:
    imag = cv2.imread("ML-trash-images/aluminum/lids/"+lid)
    img_from_ar = Image.fromarray(imag, 'RGB')
    resized_image = img_from_ar.resize((size, size))
    data.append(np.array(resized_image))
    labels.append(3)

# creating dataset for plastic bottles images
plastic_bottles = os.listdir("ML-trash-images/plastic/plastic_bottles")
for plastic_bottle in plastic_bottles:
    imag = cv2.imread("ML-trash-images/plastic/plastic_bottles/"+plastic_bottle)
    img_from_ar = Image.fromarray(imag, 'RGB')
    resized_image = img_from_ar.resize((size, size))
    data.append(np.array(resized_image))
    labels.append(4)

# creating dataset for plastic bags images
bags = os.listdir("ML-trash-images/plastic/bags")
for bag in bags:
    imag = cv2.imread("ML-trash-images/plastic/bags/"+bag)
    img_from_ar = Image.fromarray(imag, 'RGB')
    resized_image = img_from_ar.resize((size, size))
    data.append(np.array(resized_image))
    labels.append(5)

# converting and saving dataset into numpy array
trash = np.array(data)
labels = np.array(labels)
np.save("trash",trash)
np.save("labels",labels)

# loading dataset
trash = np.load("trash.npy")
labels = np.load("labels.npy")

# shuffling dataset
s = np.arange(trash.shape[0])
np.random.shuffle(s)
trash = trash[s]
labels = labels[s]

types_trash = len(np.unique(labels))
data_length = len(trash)

# creating train and test datasets
x_train = trash[(int)(0.1*data_length):]
x_test = trash[:(int)(0.1*data_length)]
x_train = x_train.astype('float32')/255
x_test = x_test.astype('float32')/255

train_length = len(x_train)
test_length = len(x_test)

# creating train and test label dataset
y_train = labels[(int)(0.1*data_length):]
y_test = labels[:(int)(0.1*data_length)]

# one-hot encoding label dataset
y_train = keras.utils.to_categorical(y_train, types_trash)
y_test = keras.utils.to_categorical(y_test, types_trash)

# building classification model
# adding increasing filter sizes helps with adding more depth to images
model= tf.keras.models.Sequential()
model.add(Conv2D(filters=16, kernel_size=2, padding="same", activation="relu", input_shape=(100,100,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=2, padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=2, padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(60, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(6, activation="softmax"))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=50, epochs=100, verbose=1)

# evaluating the model with the test dataset
score = model.evaluate(x_test, y_test, verbose=1)
print('\n', 'Test accuracy:', score[1])

# saving model into JSON file 
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")