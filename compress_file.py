import shutil
import time
from config import *


def check_directory(directory):
    directory_path = os.path.join(PATH, directory)
    if not os.path.exists(directory_path):
        logging.info('Create directory {}'.format(directory))
        os.makedirs(directory_path)


def compress_file(directory):
    small_dir = directory.split('/')[-1]
    archive_name = os.path.expanduser(os.path.join(PATH, 'compressed_file', small_dir))
    root_dir = os.path.join(PATH, directory)
    gztar_file_name = shutil.make_archive(archive_name, 'gztar', root_dir)
    print(gztar_file_name)


if __name__ == '__main__':
    logging.info('Start compressing')
    part_start = time.time()

    for i in range(BIG_PARTITION):
        for j in range(SMALL_PARTITION):
            small_partition_directory = os.path.join('{}/{}_{}'.format(i, i, j))
            check_directory(small_partition_directory)
            compress_file(small_partition_directory)

    logging.info('Finish compressing, time = {}'.format((time.time() - part_start)))