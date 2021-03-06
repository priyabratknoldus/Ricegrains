# -*- coding: utf-8 -*-
"""Untitled37.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UU2ywgZqW2JZcO_-8QWLEcwge5LlgBhi
"""
import tensorflow as tf
from keras.applications import ResNet50
from keras.layers import Dense
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow.keras as keras

# This code helps to get the training data and testing data to predict
IMAGE_SIZE = [224, 224]#Give dataset path
train = 'C:\DS\Rice Grains Model\Rice grain model\rice grain mdl\training'
test = 'C:\DS\Rice Grains Model\Rice grain model\rice grain mdl\testing'

# # useful for getting number of classes
# folders = glob('/content/drive/MyDrive/ricegrains/training*')
# print(len(folders))
num_classes = 4
# each epocs will have one forward propagation and one back ward propagation
nb_epochs = 10

# Fixed for our dataset
NUM_CLASSES = 2

# Fixed for Cats & Dogs color images
CHANNELS = 3

# we are resizing the image into 224 
IMAGE_RESIZE = 224
RESNET50_POOLING_AVERAGE = 'avg'
DENSE_LAYER_ACTIVATION = 'softmax'
OBJECTIVE_FUNCTION = 'categorical_crossentropy'

# Common accuracy metric for all outputs, but can use different metrics for different output
LOSS_METRICS = ['accuracy']

# EARLY_STOP_PATIENCE must be < NUM_EPOCHS
NUM_EPOCHS = 10
EARLY_STOP_PATIENCE = 3

# These steps value should be proper FACTOR of no.-of-images in train & valid folders respectively
# Training images processed in each step would be no.-of-train-images / STEPS_PER_EPOCH_TRAINING
STEPS_PER_EPOCH_TRAINING = 10
STEPS_PER_EPOCH_VALIDATION = 10

# These steps value should be proper FACTOR of no.-of-images in train & valid folders respectively
# NOTE that these BATCH* are for Keras ImageDataGenerator batching to fill epoch step input
BATCH_SIZE_TRAINING = 100
BATCH_SIZE_VALIDATION = 100

tf.keras.applications.resnet50.ResNet50(
    include_top=True, weights='imagenet', input_tensor=None,
    input_shape=None, pooling=None, classes=1000
)

resnet=ResNet50(include_top=False, weights='imagenet',input_shape=IMAGE_SIZE + [3])

from tensorflow.keras.models import Model,Sequential
model = Sequential()

# 1st layer as the lumpsum weights from resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5
# NOTE that this layer will be set below as NOT TRAINABLE, i.e., use it as is
model.add(ResNet50(include_top = False, pooling = RESNET50_POOLING_AVERAGE, weights = 'imagenet'))

# 2nd layer as Dense for 2-class classification, i.e., dog or cat using SoftMax activation
model.add(Dense(NUM_CLASSES, activation = DENSE_LAYER_ACTIVATION))

# Say not to train first layer (ResNet) model as it is already trained
model.layers[0].trainable = False

model.summary()

from tensorflow.keras import optimizers

sgd = optimizers.SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(optimizer = sgd, loss = OBJECTIVE_FUNCTION, metrics = LOSS_METRICS)

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

image_size = IMAGE_RESIZE

data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator = data_generator.flow_from_directory(
        '/content/drive/MyDrive/ricegrains/training',
        target_size=(image_size, image_size),
        batch_size=BATCH_SIZE_TRAINING,
        class_mode='categorical')


validation_generator = data_generator.flow_from_directory(
        '/content/drive/MyDrive/ricegrains/testing',
        target_size=(image_size, image_size),
        batch_size=BATCH_SIZE_VALIDATION,
        class_mode='categorical')

# Data Augmentation
train_datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')


# Data Augmentation
test_datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

fit_history = model.fit_generator(
        train_generator,
        steps_per_epoch=STEPS_PER_EPOCH_TRAINING,
        epochs = NUM_EPOCHS,
        validation_data=validation_generator,
        validation_steps=STEPS_PER_EPOCH_VALIDATION
        
)

model.save("ricegrains.h5")
print("Saved model to disk")

import numpy as np

from tensorflow.keras.preprocessing import image

from tensorflow.python.keras.models import load_model

test_image = image.load_img('C:\DS\Rice Grains Model\Rice grain model\rice grain mdl\goodrice_0_1996.jpg', target_size = (224, 224,3))

test_image

test_image = image.img_to_array(test_image)

test_image = np.expand_dims(test_image, axis = 0)

model = load_model('ricegrains.h5')

result = model.predict(test_image)

result = result[0]

classes = ['good rice grains','bad rice grains']

label_name = {classes[i]: result[i] for i in range(len(result))}
label_name

