from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.models import Sequential
from keras.models import Model
from keras.layers import *
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D , MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras_applications.imagenet_utils import get_submodules_from_kwargs
from keras_applications.imagenet_utils import _obtain_input_shape

import keras_applications.imagenet_utils as imagenet_utils
import keras.backend as backend
import keras.models as models
import keras.layers as layers
import keras.utils as utils

import os
import keras
import cv2, numpy as np

def multipleInputDataModel(mplOut, cnnOut, mplIn, cnnIn, nOutPut):
    inputConcat = keras.layers.Concatenate()([mplOut, cnnOut])
    x = Dense(68, activation="relu")(inputConcat)
    x = Dense(nOutPut, activation="relu")(x)
    model = Model(inputs=[mplIn, cnnIn], outputs=x)

    return model
    
def mplModel(inputShape, nOutPut):
    inputT = Input(shape=inputShape)
    x = Dense(68, activation="relu")(inputT)
    x = Flatten()(x)
    x = Dense(nOutPut, activation="relu")(x)

    model = Model(inputs=inputT, outputs=x)

    return inputT, x

def basicCNNModel(inputShape, nOutPut):
    inputT = Input(shape=inputShape)

    #1st convolution layer
    x = Conv2D(128, (3, 3), activation='relu', input_shape=inputShape)(inputT)
    x = MaxPooling2D(pool_size=(5,5), strides=(2, 2))(x)

    #2nd convolution layer
    x = Conv2D(256, (3, 3), activation='relu')(x)
    x = Conv2D(256, (3, 3), activation='relu')(x)
    x = AveragePooling2D(pool_size=(3,3), strides=(1, 1))(x)

    #3rd convolution layer
    x = Conv2D(512, (3, 3), activation='relu')(x)
    x = Conv2D(512, (3, 3), activation='relu')(x)
    x = AveragePooling2D(pool_size=(3,3), strides=(1, 1))(x)

    x = Flatten()(x)

    #fully connected neural networks
    x = Dense(nOutPut, activation='relu')(x)
    x = Dense(nOutPut, activation='relu')(x)
    
    model = Model(inputs=inputT, outputs=x)

    return inputT, x


def VGG16(input_shape,
          classes,
          include_top=True,
          input_tensor=None,
          pooling=None,
          **kwargs):
    """Instantiates the VGG16 architecture.
    Optionally loads weights pre-trained on ImageNet.
    Note that the data format convention used by the model is
    the one specified in your Keras config at `~/.keras/keras.json`.
    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization),
              'imagenet' (pre-training on ImageNet),
              or the path to the weights file to be loaded.
        input_tensor: optional Keras tensor
            (i.e. output of `layers.Input()`)
            to use as image input for the model.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False (otherwise the input shape
            has to be `(224, 224, 3)`
            (with `channels_last` data format)
            or `(3, 224, 224)` (with `channels_first` data format).
            It should have exactly 3 input channels,
            and width and height should be no smaller than 32.
            E.g. `(200, 200, 3)` would be one valid value.
        pooling: Optional pooling mode for feature extraction
            when `include_top` is `False`.
            - `None` means that the output of the model will be
                the 4D tensor output of the
                last convolutional block.
            - `avg` means that global average pooling
                will be applied to the output of the
                last convolutional block, and thus
                the output of the model will be a 2D tensor.
            - `max` means that global max pooling will
                be applied.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.
    # Returns
        A Keras model instance.
    # Raises
        ValueError: in case of invalid argument for `weights`,
            or invalid input shape.
    """
    
    # Determine proper input shape
    input_shape = _obtain_input_shape(input_shape,
                                      default_size=224,
                                      min_size=32,
                                      data_format=backend.image_data_format(),
                                      require_flatten=include_top)

    if input_tensor is None:
        img_input = layers.Input(shape=input_shape)
        
    # Block 1
    x = layers.Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv1')(img_input)
    x = layers.Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv2')(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = layers.Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv1')(x)
    x = layers.Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv2')(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv1')(x)
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv2')(x)
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv3')(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv1')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv2')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv3')(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv1')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv2')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv3')(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    if include_top:
        # Classification block
        x = layers.Flatten(name='flatten2')(x)
        x = layers.Dense(4096, activation='relu', name='fc1')(x)
        x = layers.Dense(4096, activation='relu', name='fc2')(x)
        x = layers.Dense(classes, activation='softmax', name='predictions')(x)
    else:
        if pooling == 'avg':
            x = layers.GlobalAveragePooling2D()(x)
        elif pooling == 'max':
            x = layers.GlobalMaxPooling2D()(x)


    inputs = img_input

    # Create model.
    model = models.Model(inputs, x, name='vgg16')

    return inputs, x 