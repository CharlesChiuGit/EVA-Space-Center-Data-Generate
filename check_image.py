import cv2
from glob import glob
from helper_function import *
from config import *


# DATASET_AMOUNT = 200000
# DATASET_NAME = 'Dataset_fovy120'
# BIG_PARTITION = 10
# SMALL_PARTITION = 10
# IMAGES_PER_SMALL_PARTITION = 2000


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
        print(i)
        for j in range(10):
            images_path = dataset_path + '%d/%d_%d/' % (i, i, j)
            images = glob(images_path + '%s*' % DATASET_NAME)
            if len(images) != DATASET_AMOUNT / 100:
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
            if len(images) != DATASET_AMOUNT / 100:
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
            if len(images) != DATASET_AMOUNT / 100:
                error_messages.append('Number of images incorrect: %s = %d' % (images_path, len(images)))
            for image in images:
                img = cv2.imread(image, 0)
                try:
                    cv2.pyrDown(img)
                except Exception as e:
                    error_messages.append('CRC Error: %s' % image)
                    replace_local_image_with_original_image(image)

    return error_messages


def build_path_from_image_index(image_path):
    file_name = remove_extra_path(image_path)
    image_name = remove_filename_extension(file_name)
    image_index = int(get_image_index(image_name))
    folder_index = int(image_index / IMAGES_PER_SMALL_PARTITION)
    big_index = int(folder_index / BIG_PARTITION)
    small_index = (folder_index % BIG_PARTITION)
    remote_image_path = "/data/{}/{}/{}_{}/{}".format(DATASET_NAME, big_index, big_index, small_index, file_name)
    logging.info('Remote path rebuild: {}'.format(remote_image_path))
    return remote_image_path


def replace_local_image_with_original_image(defective_image_path):
    remote_image_path = build_path_from_image_index(defective_image_path)
    download_file_from_remote_device(remote_image_path, defective_image_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')
    check_dataset_images()
    # file_path = "/data/Dataset_fovy120/train/images/4/4_4/Dataset_fovy120_89999.png"
    # replace_local_image_with_original_image(file_path)
