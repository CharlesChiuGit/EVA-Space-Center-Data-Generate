import os
import logging
import argparse
# set SDL to use the dummy NULL video driver,
#   so it doesn't need a windowing system.
# os.environ["SDL_VIDEODRIVER"] = "dummy"


def set_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dn', '--dataset_name', help='Set Dataset name')
    parser.add_argument('-o', '--object', help='Choose a object model')
    parser.add_argument('-d', '--defect_img_name', help='Give the defect image name')
    parser.add_argument('-i', '--target_index', help='Set target index')
    parser.add_argument('-n', '--total_number', help='Set total number of dataset')
    parser.add_argument('-lv1', '--level_1_index', help='Set level_1_index')
    parser.add_argument('-lv2', '--level_2_index', help='Set level_2_index')

    return parser.parse_args()


# Set logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')

# Dateset name
args = set_argument_parser()
DATASET_NAME = args.dataset_name
SINGLE_IMAGE = args.defect_img_name
if args.defect_img_name:
    logging.info('Defect Image Name: {}'.format(args.defect_img_name))
TARGET_INDEX = args.target_index
OBJECT = args.object

# Units
UNIT_REAL = 996.679647  # in km
MOON_RADIUS = 1.742887
OPENGL_1_METER = 0.001 / UNIT_REAL

# Constraints
VIEWPORT = [800, 600]
FOVY = 5  # in degrees
Z_NEAR = 1.0
Z_FAR = 100.0
LOWER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 200)  # 200m above moon surface
UPPER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 30000)  # 30,000m above moon surface

# PATH
PATH = os.path.join('/data', DATASET_NAME)
if not os.path.exists(PATH):
    logging.info('Create dataset {}'.format(DATASET_NAME))
    os.makedirs(PATH)
PATCH_PATH = '/home/eva/space_center/moon_8K/Single_Image/'

# hyperparameters
TOTAL_IMAGE_NUM = int(args.total_number)
LEVEL_1_INDEX = int(args.level_1_index)
LEVEL_2_INDEX = int(args.level_2_index)
IMAGE_INDEX = (TOTAL_IMAGE_NUM / LEVEL_1_INDEX) / LEVEL_2_INDEX
