import cv2
from glob import glob
from config import *


IMAGE_NUM = 200000
DATASET_NAME = 'Dataset_fovy120'


def check_dataset_images():
    error_messages = []
    logging.info('Check images of dataset')

    logging.info('Check train dataset')
    error_messages += check_train_images()
    logging.info('Check test dataset')
    error_messages += check_test_images()
    logging.info('Check validation dataset')
    error_messages += check_validation_images()

    if not error_messages:
        logging.info('Finish checking images of dataset')
    else:
        logging.error('Some error happened')
        for error_message in error_messages:
            logging.error(error_message)


def check_train_images():
    error_messages = []
    dataset_path = '/data/space/' + DATASET_NAME + '/train/images/'
    for i in range(8):
        for j in range(10):
            images_path = dataset_path + '%d/%d_%d/' % (i, i, j)
            images = glob(images_path + '%s*' % DATASET_NAME)
            if len(images) != IMAGE_NUM / 100:
                error_messages.append('Number of images incorrect: %s = %d' % (images_path, len(images)))
            for image in images:
                img = cv2.imread(image, 0)
                try:
                    cv2.pyrDown(img)
                except Exception as e:
                    error_messages.append('Pyrdown error %s image = %s' % (str(e), image))
                    replace_local_image_with_original_image(image)

    return error_messages


def check_test_images():
    error_messages = []
    dataset_path = '/data/space/' + DATASET_NAME + '/test/images/'
    for i in range(1):
        for j in range(10):
            images_path = dataset_path + '%d/%d_%d/' % (i, i, j)
            images = glob(images_path + '%s*' % DATASET_NAME)
            if len(images) != IMAGE_NUM / 100:
                error_messages.append('Number of images incorrect: %s = %d' % (images_path, len(images)))
            for image in images:
                img = cv2.imread(image, 0)
                try:
                    cv2.pyrDown(img)
                except Exception as e:
                    error_messages.append('CRC Error: %s' % image)
                    replace_local_image_with_original_image(image)

    return error_messages


def check_validation_images():
    error_messages = []
    dataset_path = '/data/space/' + DATASET_NAME + '/validation/images/'
    for i in range(1):
        for j in range(10):
            images_path = dataset_path + '%d/%d_%d/' % (i, i, j)
            images = glob(images_path + '%s*' % DATASET_NAME)
            if len(images) != IMAGE_NUM / 100:
                error_messages.append('Number of images incorrect: %s = %d' % (images_path, len(images)))
            for image in images:
                img = cv2.imread(image, 0)
                try:
                    cv2.pyrDown(img)
                except Exception as e:
                    error_messages.append('CRC Error: %s' % image)
                    replace_local_image_with_original_image(image)

    return error_messages


def replace_local_image_with_original_image(defect_image_path):
    ##TODO

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')
    check_dataset_images()