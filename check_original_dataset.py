import cv2
from glob import glob
from config import *
from regenerate_defect_image import regenerate_defective_image


def check_dataset_images():
    error_messages = []
    logging.info('Check images of dataset')

    logging.info('Check original dataset')
    error_messages += check_original_images()

    if not error_messages:
        logging.info('Finish checking images of dataset')
    else:
        logging.error('Some error happened')
        for error_message in error_messages:
            logging.error(error_message)


def check_original_images():
    error_messages = []
    dataset_path = '/data/' + DATASET_NAME + '/'
    for i in range(BIG_PARTITION):
        print(i)
        for j in range(SMALL_PARTITION):
            images_path = dataset_path + '%d/%d_%d/' % (i, i, j)
            images = glob(images_path + '%s*' % DATASET_NAME)
            if len(images) != DATASET_AMOUNT / (SMALL_PARTITION * BIG_PARTITION):
                error_messages.append('Number of images incorrect: %s = %d' % (images_path, len(images)))
            for image in images:
                img = cv2.imread(image, 0)
                try:
                    cv2.pyrDown(img)
                except Exception as e:
                    error_messages.append('Pyrdown error %s image = %s' % (str(e), image))
                    regenerate_defective_image(image)

    return error_messages


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')
    check_dataset_images()
    # file_path = "/data/Dataset_fovy120/train/images/4/4_4/Dataset_fovy120_89999.png"
    # replace_local_image_with_original_image(file_path)
