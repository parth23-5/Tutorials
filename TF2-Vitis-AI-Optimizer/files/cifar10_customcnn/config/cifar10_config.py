#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2023 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Author: Daniele Bagni, Xilinx Inc
# date:  29 July 2023


import os
#https://bobbyhadz.com/blog/disable-suppress-tensorflow-warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import logging
#https://github.com/tensorflow/tensorflow/issues/8340
logging.getLogger("tensorflow").setLevel(logging.WARNING)

import numpy as np

###############################################################################
# project folders
###############################################################################

def get_script_directory():
    path = os.getcwd()
    return path

# get current directory
SCRIPT_DIR = get_script_directory()

# dataset top level folder
DATASET_DIR = os.path.join(SCRIPT_DIR, "./dataset/cifar10")
# train, validation, test and calibration folders
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VALID_DIR = os.path.join(DATASET_DIR, "valid")
TEST_DIR  = os.path.join(DATASET_DIR, "test")
CALIB_DIR = os.path.join(SCRIPT_DIR, "./dataset/cifar10/calib")

###############################################################################
# global variables
###############################################################################

# since we do not have validation data or access to the testing labels we need
# to take a number of images from the training data and use them instead
NUM_CLASSES      =    10
NUM_VAL_IMAGES   =  5000
NUM_TEST_IMAGES  =  5000
NUM_TRAIN_IMAGES = 50000

#Size of images
IMAGE_WIDTH  = 32
IMAGE_HEIGHT = 32

#normalization factor to scale image 0-255 values to 0-1 #DB
NORM_FACTOR = 255 # could be also 256.0

# label names for the FASHION MNIST dataset
labelNames_dict = { "airplane" : 0, "automobile" : 1, "bird" : 2, "cat" : 3, "deer" : 4, "dog" : 5,
                    "frog" : 6, "horse" : 7, "ship" : 8, "truck" : 9}
labelNames_list = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]


# miniVggNet build parameters
input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT,3)
classes=NUM_CLASSES


DIVIDER = '-----------------------------------------'

# Training
BATCH_SIZE=32 #128
train_init_lr=0.001
# train_epochs= 15 # to stop at 83% accuracy
train_epochs= 50   # to stop at 84% accuracy
train_target_acc=1.0
train_output_ckpt="/float_model/f_model.h5"

#pre_trained_cifar10="/../float_model/orig_f_model.h5"


# Pruning & Fine-tuning
prune_output_ckpt="/pruned_model/p_model"
init_prune_ratio=0.1
incr_prune_ratio=0.1
prune_steps=6
finetune_init_lr=0.0007

# Transform
transform_output_ckpt="/transform_model/t_model.h5"

# Quantization
quant_output_ckpt="/quant_model/q_model.h5"

# Compile
compile_dir="/compiled_model_"
#model_name="miniVggNet"
model_name="minicnn"

# Target
target_dir="/target_"

# Application code
app_dir="application"

# CNN: either ResNet18 or miniVggNet
cnn="ResNet18"


###############################################################################
# global functions
###############################################################################

'''
import cv2

_R_MEAN = 0
_G_MEAN = 0
_B_MEAN = 0

MEANS = np.array([_B_MEAN,_G_MEAN,_R_MEAN],np.dtype(np.int32))

def mean_image_subtraction(image, means):
  B, G, R = cv2.split(image)
  B = B - means[0]
  G = G - means[1]
  R = R - means[2]
  image = cv2.merge([R, G, B])
  return image
'''

def Normalize(x_test):
    x_test = x_test/NORM_FACTOR
    x_test = x_test -0.5
    out_x_test = x_test *2
    #out_x_test = x_test
    return out_x_test


def ScaleTo1(x_test):
    x_test  = np.asarray(x_test)
    x_test = x_test.astype(np.float32)
    our_x_test = x_test/NORM_FACTOR
    return out_x_test
