import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

sys.path.append(ROOT_DIR)
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log
%matplotlib inline

MODEL_DIR = os.path.join(ROOT_DIR, "logs")
WEIGHTS_PATH = "/content/wastedata-Mask_RCNN-multiple-classes/main/Mask_RCNN/logs/object20210725T1652/mask_rcnn_object_0013.h5"  # TODO: update this path
config = CustomConfig()
CUSTOM_DIR = os.path.join(ROOT_DIR, "./dataset/")
class InferenceConfig(config.__class__):

DEVICE = "/gpu:0" 

TEST_MODE = "inference"
def get_ax(rows=1, cols=1, size=16):
  _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
  return ax

# Загружаем валидационный датасет
CUSTOM_DIR = "./dataset"
dataset = CustomDataset()
dataset.load_custom(CUSTOM_DIR, "val")

dataset.prepare()
print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))

# загружаем модель
with tf.device(DEVICE):
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
  
print("Loading weights ", WEIGHTS_PATH)
model.load_weights(WEIGHTS_PATH, by_name=True)