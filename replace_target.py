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

    return data.keys(), data


if __name__ == '__main__':
    local_dataset_path = '/data/Dataset_all_random'
    patch_path = '/home/eva/space_center/moon_8K/Single_Image/'
    new_labels_path = os.path.join(patch_path, 'target_' + DATASET_NAME + '_*.json')
    new_label_files = sorted(glob(new_labels_path))
    old_labels_path = os.path.join(local_dataset_path, 'target_' + sys.argv[2] + '.json')
    print(new_label_files)
    key, data = read_json(old_labels_path)
    print(key[-1])
    # print(data)
    for i in range(len(new_label_files)):
        [new_key], data = read_json(new_label_files[i])

