#!/bin/bash

dataset_name='Dataset_test_1'
remote_dataset_path="/data/${dataset_name}"
remote_IP='eva@140.113.86.59'
local_dataset_path="/data/space/${dataset_name}"
local_private_key="$HOME/.ssh/eva_58"
file_type=('train' 'test' 'validation' 'compressed_file')
data_type=('images' 'labels')
git pull
# ----------------------------------------------

chech_partical_dataset(){
  type=$1
  index=$2
  image_file="${local_dataset_path}/${type}/${data_type[0]}"
  mkdir -m 777 -v "${image_file}/${index}"
  label_file="${local_dataset_path}/${type}/${data_type[1]}"
  mv "${local_dataset_path}/target_${index}.json"  "${label_file}"
  echo "${index}"
  for j in $(seq 0 9)
  do
    mkdir -m 777 -v "${image_file}/${index}/${index}_$j"
    tar -C "${image_file}/${index}/${index}_$j" -zxf "${local_dataset_path}/${file_type[3]}/${index}_$j.tar.gz"
    for img in "${image_file}/${index}/${index}_$j"/*.png
    do
      pngcheck -q "$img"
      retval=$?
      if [ $retval -ne 0 ]; then
        replace_defect_img_name "$img"
      fi
    done
  done
}


replace_defect_img_name(){
  local_image_path=$1
  OIFS="$IFS"
  IFS='/'
  read -r -a new_list <<< "${local_image_path}"
  IFS="$OIFS"
  remote_image_path="${remote_IP}:${remote_dataset_path}/${new_list[3]}/${new_list[4]}/${new_list[5]}"
  scp -i "${local_private_key}" "${remote_image_path}" "${local_image_path}"
  echo "Error ${img} replaced!"
}
# ----------------------------------------------

echo 'Start building local dataset'
mkdir -m 777 -v "${local_dataset_path}"
mkdir -m 777 -v "${local_dataset_path}/${file_type[3]}"
scp -i "${local_private_key}" "${remote_IP}:${remote_dataset_path}/*.tar.gz" "${local_dataset_path}/${file_type[3]}"
scp -i "${local_private_key}" "${remote_IP}:${remote_dataset_path}/tar*" "${local_dataset_path}"
# ----------------------------------------------

echo 'Start decompressing'

for i in $(seq 0 2)
do
  mkdir -m 777 -v "${local_dataset_path}/${file_type[i]}"
  mkdir -m 777 -v "${local_dataset_path}/${file_type[i]}/${data_type[0]}"
  mkdir -m 777 -v "${local_dataset_path}/${file_type[i]}/${data_type[1]}"
done

echo "checking train dataset"
for i in $(seq 0 7); do chech_partical_dataset "${file_type[0]}" "$i"; done

echo "checking test dataset"
chech_partical_dataset "${file_type[1]}" "8"

echo "checking validation dataset"
chech_partical_dataset "${file_type[2]}" "9"

echo 'End decompressing'
echo 'End building local dataset'

#train_image_file="${local_dataset_path}/${file_type[0]}/${data_type[0]}"
#tar -C "${train_image_file}/4/4_6" -zxf "${local_dataset_path}/compressed_file/4_6.tar.gz"
#tar -C "${train_image_file}/7/7_6" -zxf "${local_dataset_path}/compressed_file/7_6.tar.gz"
#tar -C "${image_file}/4/4_5" -zxf "${local_dataset_path}/compressed_file/4_5.tar.gz"
#tar -C "${image_file}/6/6_3" -zxf "${local_dataset_path}/compressed_file/6_3.tar.gz"
#tar -C "${image_file}/6/6_4" -zxf "${local_dataset_path}/compressed_file/6_4.tar.gz"
#echo 'End decompressing'
#pngcheck -q "/data/space/Dataset_six_random/train/images/4/4_6/Dataset_six_random_92664.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/7/7_6/Dataset_six_random_152692.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/4/4_5/Dataset_six_random_90538.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/6/6_3/Dataset_six_random_127609.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/6/6_4/Dataset_six_random_128244.png"