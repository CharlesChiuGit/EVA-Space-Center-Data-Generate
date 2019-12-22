import cv2
import json
import logging
import math
import numpy as np
import os
import shutil
import sys
from glob import glob
import ntpath
from config import *


def path_leaf(path):
    head, tail = ntpath.split(path)

    return tail or ntpath.basename(head)


def read_json(file_path):
    with open(file_path, 'r') as reader:
        data = json.loads(reader.read())

    print(data.keys()[0])
    return data


if __name__ == '__main__':
    local_dataset_path = '/data/Dataset_all_random'
    patch_path = '/home/eva/space_center/moon_8K/Single_Image/'
    image_path = os.path.join(patch_path, DATASET_NAME + '_*.png')
    image_files = sorted(glob(image_path))
    labels_path = os.path.join(patch_path, 'target_' + DATASET_NAME + '_*.json')
    label_files = sorted(glob(labels_path))
    print(label_files)
    print(label_files[0])
    data = read_json(label_files[0])
