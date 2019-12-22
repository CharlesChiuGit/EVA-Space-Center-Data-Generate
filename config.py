import os
import sys
import logging

# Set logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')
teamviewer_password = 'jy2u27'

# Dateset name
DATASET_NAME = 'Dataset_all_random'
if sys.argv[2]:
    SINGLE_IMAGE = sys.argv[2]
else:
    print("ERROR: SINGLE_IMAGE is not given!")

# Units
UNIT_REAL = 996.679647  # in km
MOON_RADIUS = 1.742887
OPENGL_1_METER = 0.001 / UNIT_REAL

# Constraints
VIEWPORT = [800, 600]
FOVY = 90.0  # in degrees
Z_NEAR = 1.0
Z_FAR = 100.0
LOWER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 200)  # 200m above moon surface
UPPER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 10000)  # 10,000m above moon surface

# PATH
if sys.argv[2]:
    PATH = '/home/eva/space_center/moon_8K/Single_Image/'
else:
    PATH = os.path.join('/data/', DATASET_NAME)
    if not os.path.exists(PATH):
        logging.info('Create dataset {}'.format(DATASET_NAME))
        os.makedirs(PATH)

# hyperparameters
TOTAL_IMAGE_NUM = 200000
LEVEL_1_INDEX = 10
LEVEL_2_INDEX = 10
IMAGE_INDEX = (TOTAL_IMAGE_NUM / LEVEL_1_INDEX) / LEVEL_2_INDEX
