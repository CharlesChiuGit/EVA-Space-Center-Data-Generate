#!/bin/bash

local_dataset_path='/data/Dataset_all_random'
single_img_folder='/home/eva/space_center/moon_8K/Single_Image/'
object="Moon_8K.obj"

echo 'Start checking original dataset'

for i in $(seq 0 9)
do
  for j in $(seq 0 9)
  do
    for img in $(ls "${local_dataset_path}/$i/${i}_$j/")
    do
      pngcheck -q "${local_dataset_path}/$i/${i}_$j/$img"
      retval=$?
      if [ $retval -ne 0 ]; then
        echo "${img}"
      fi
      python generate_single_image.py -s ${img} ${object}

    done
  done
done

#echo 'End checking original dataset'
#
#img="Dataset_all_random_50377.png"
#pngcheck -q "${local_dataset_path}/5/5_0/${img}"
#retval=$?
#if [ $retval -ne 0 ]; then
#  echo "${img}"
#fi