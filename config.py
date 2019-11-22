import os
import logging

# Set logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')

# Dateset name
DATASET_NAME = 'Dataset_all_random'

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
UPPER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 10000)   # 10,000m above moon surface

# PATH
PATH = os.path.join('/data/', DATASET_NAME)
if not os.path.exists(PATH):
    os.makedirs(PATH)

# hyperparameters
LEVEL_1_INDEX = 1
LEVEL_2_INDEX = 1
IMAGE_INDEX = 1000
