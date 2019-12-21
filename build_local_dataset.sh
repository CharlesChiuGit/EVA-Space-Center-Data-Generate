#!/bin/bash

remote_dataset_path='/data/Dataset_six_random'
remote_IP='eva@140.113.86.59'
local_dataset_path='/data/space/Dataset_six_random'
local_private_key='../.ssh/eva_58'
file_type=('train' 'test' 'validation' 'compressed_file')
data_type=('images' 'labels')

echo 'Start building local dataset'
mkdir -m 777 -v "${local_dataset_path}"
mkdir -m 777 -v "${local_dataset_path}/${file_type[3]}"
scp -i ${local_private_key} ${remote_IP}:${remote_dataset_path}/*.tar.gz "${local_dataset_path}/${file_type[3]}"
scp -i ${local_private_key} ${remote_IP}:${remote_dataset_path}/tar* "${local_dataset_path}"

for i in $(seq 0 2)
do
  mkdir -m 777 -v "${local_dataset_path}/${file_type[i]}"
  mkdir -m 777 -v "${local_dataset_path}/${file_type[i]}/${data_type[0]}"
  mkdir -m 777 -v "${local_dataset_path}/${file_type[i]}/${data_type[1]}"
done

echo 'Start decompressing'
for i in $(seq 0 7)
do
  train_image_file="${local_dataset_path}/${file_type[0]}/${data_type[0]}"
  mkdir -m 777 -v "${train_image_file}/$i"
  train_label_file="${local_dataset_path}/${file_type[0]}/${data_type[1]}"
  mv "${local_dataset_path}/target_$i.json"  "${train_label_file}"
  for j in $(seq 0 9)
  do
    mkdir -m 777 -v "${train_image_file}/$i/${i}_$j"
    tar -C "${train_image_file}/$i/${i}_$j" -zxf "${local_dataset_path}/${file_type[3]}/${i}_$j.tar.gz"
    for img in $(ls "${train_image_file}/$i/${i}_$j/")
    do
#      echo "${train_image_file}/$i/${i}_$j/$img"
      pngcheck -q "${train_image_file}/$i/${i}_$j/$img"
    done
  done
done

test_image_file="${local_dataset_path}/${file_type[1]}/${data_type[0]}"
mkdir -m 777 -v "${test_image_file}/0"
test_label_file="${local_dataset_path}/${file_type[1]}/${data_type[1]}"
mv "${local_dataset_path}/target_8.json"  "${test_label_file}"
for j in $(seq 0 9)
do
  mkdir -m 777 -v "${test_image_file}/0/0_$j"
  tar -C "${test_image_file}/0/0_$j" -zxf "${local_dataset_path}/${file_type[3]}/8_$j.tar.gz"
  for img in $(ls "${test_image_file}/0/0_$j/")
  do
#    echo "${test_image_file}/0/0_$j/$img"
    pngcheck -q "${test_image_file}/0/0_$j/$img"
  done
done

validation_image_file="${local_dataset_path}/${file_type[2]}/${data_type[0]}"
mkdir -m 777 -v "${validation_image_file}/0"
validation_label_file="${local_dataset_path}/${file_type[2]}/${data_type[1]}"
mv "${local_dataset_path}/target_9.json"  "${validation_label_file}"
for j in $(seq 0 9)
do
  mkdir -m 777 -v "${validation_image_file}/0/0_$j"
  tar -C "${validation_image_file}/0/0_$j" -zxf "${local_dataset_path}/${file_type[3]}/9_$j.tar.gz"
  for img in $(ls "${validation_image_file}/0/0_$j/")
  do
#    echo "${validation_image_file}/0/0_$j/$img"
    pngcheck -q "${validation_image_file}/0/0_$j/$img"
  done
done
echo 'End decompressing'
echo 'End building local dataset'

#echo 'Start checking dataset'
#image_file="${local_dataset_path}/${file_type[1]}/${data_type[0]}"
#for j in $(seq 0 9)
#do
#    for img in $(ls "${image_file}/0/0_$j/")
#    do
#      echo "${image_file}/0/0_$j/$img"
#      pngcheck -q "${image_file}/0/0_$j/$img"
#    done
#done
#echo 'End checking dataset'

#tar -C "${image_file}/0/0_0" -zxf "${local_dataset_path}/compressed_file/0_0.tar.gz"
#tar -C "${image_file}/2/2_8" -zxf "${local_dataset_path}/compressed_file/2_8.tar.gz"
#tar -C "${image_file}/4/4_5" -zxf "${local_dataset_path}/compressed_file/4_5.tar.gz"
#tar -C "${image_file}/6/6_3" -zxf "${local_dataset_path}/compressed_file/6_3.tar.gz"
#tar -C "${image_file}/6/6_4" -zxf "${local_dataset_path}/compressed_file/6_4.tar.gz"
#echo 'End decompressing'
#pngcheck -q "/data/space/Dataset_six_random/train/images/0/0_0/Dataset_six_random_75.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/2/2_8/Dataset_six_random_56129.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/4/4_5/Dataset_six_random_90538.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/6/6_3/Dataset_six_random_127609.png"
#pngcheck -q "/data/space/Dataset_six_random/train/images/6/6_4/Dataset_six_random_128244.png"