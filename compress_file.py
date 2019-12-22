import shutil
import time
from config import *


def check_directory(directory):
    directory_path = os.path.join(PATH, directory)
    if not os.path.exists(directory_path):
        logging.info('Create directory {}'.format(directory))
        os.makedirs(directory_path)


def compress_file(directory):
    archive_name = os.path.expanduser(os.path.join(PATH, 'compress_file', directory))
    root_dir = os.path.join(PATH, directory)
    gztar_file_name = shutil.make_archive(archive_name, 'gztar', root_dir)
    print(gztar_file_name)


if __name__ == '__main__':
    logging.info('Start compressing')
    part_start = time.time()

    for i in range(LEVEL_1_INDEX):
        level_l_directory = '{}'.format(i)
        check_directory(level_l_directory)
        for j in range(LEVEL_2_INDEX):
            level_2_directory = os.path.join(level_l_directory, '{}_{}'.format(i, j))
            check_directory(level_2_directory)
            compress_file(level_2_directory)

    logging.info('Finish compressing, time = {}'.format((time.time() - part_start)))