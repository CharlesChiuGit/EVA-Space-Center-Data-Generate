import os
import logging
import argparse


# set SDL to use the dummy NULL video driver,
#   so it doesn't need a windowing system.
# os.environ["SDL_VIDEODRIVER"] = "dummy"


def set_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dn', '--dataset_name', help='Set Dataset name')
    parser.add_argument('-o', '--object', default='Moon_8K.obj', help='Choose a object model')
    parser.add_argument('-d', '--defect_img_name', default='Dataset_test_0.png', help='Give the defect image name')
    parser.add_argument('-i', '--target_index', default=000, help='Which target index, target_X.json')
    parser.add_argument('-n', '--total_number', default=1, help='Total number of dataset')
    parser.add_argument('-lv1', '--level_1_index', default=1, help='How many partial you want to divide')
    parser.add_argument('-lv2', '--level_2_index', default=1, help='How many smaller partial you want to divide')
    parser.add_argument('-e', '--do_experiment', action="store_true", default='False',
                        help='Set True if you want to do experiment')
    parser.add_argument('-en', '--experiment_name', default='test', help='Generate single experiment image')

    return parser.parse_args()


# Set logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')

# Dateset name
args = set_argument_parser()
OBJECT = args.object
if not args.do_experiment:
    DATASET_NAME = args.dataset_name
    TARGET_INDEX = args.target_index
    SINGLE_IMAGE = args.defect_img_name
    if args.defect_img_name:
        logging.info('Defect Image Name: {}'.format(args.defect_img_name))

OBJECT = args.object

# Units
UNIT_REAL = 996.679647  # in km
MOON_RADIUS = 1.742887
OPENGL_1_METER = 0.001 / UNIT_REAL

# Constraints
VIEWPORT = [800, 600]
FOVY = 120  # in degrees
Z_NEAR = 1.0
Z_FAR = 100.0
LOWER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 200)  # 200m above moon surface
UPPER_BOUND = MOON_RADIUS + (OPENGL_1_METER * 10000)  # 10,000m above moon surface

# PATH
if not args.do_experiment:
    PATH = os.path.join('/data', DATASET_NAME)
    PATCH_PATH = '~eva/space_center/moon_8K/Regen_Image/'
    if not os.path.exists(PATH):
        logging.info('Create dataset {}'.format(DATASET_NAME))
        os.makedirs(PATH)

# hyperparameters
TOTAL_IMAGE_NUM = int(args.total_number)
LEVEL_1_INDEX = int(args.level_1_index)
LEVEL_2_INDEX = int(args.level_2_index)
IMAGE_INDEX = (TOTAL_IMAGE_NUM / LEVEL_1_INDEX) / LEVEL_2_INDEX

# Experiment
if args.do_experiment:
    logging.info('Do Experiment')
    EXPERIMENT_PATH = '~/space_center/moon_8K/Experiment/'
    EXPERIMENT_IMAGE = args.experiment_name
