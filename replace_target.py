import json
from glob import glob
from config import *


def read_json(file_path):
    with open(file_path, 'r') as reader:
        data = json.loads(reader.read())

    return data.keys(), data


if __name__ == '__main__':
    local_dataset_path = '/data/Dataset_all_random'
    patch_path = '/home/eva/space_center/moon_8K/Single_Image/'
    new_labels_path = os.path.join(patch_path, 'target_' + DATASET_NAME + '_*.json')
    new_label_files = sorted(glob(new_labels_path))
    old_label_path = os.path.join(local_dataset_path, 'target_' + sys.argv[2] + '.json')
    print(new_label_files)
    print(old_label_path)
    keys, datas = read_json(old_label_path)
    for i in range(len(new_label_files)):
        [new_key], new_data = read_json(new_label_files[i])
        print('New data: ', new_data[new_key]['spherical'])
        for key in keys:
            if key == new_key:
                datas[new_key] = new_data[new_key]['spherical']
    print('Renew data: ', datas[new_key])
    with open(old_label_path, 'w') as f:
        json.dump(datas, f)
        logging.info('Finish saving {}'.format(old_label_path))



