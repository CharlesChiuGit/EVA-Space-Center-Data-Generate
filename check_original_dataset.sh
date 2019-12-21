#!/bin/bash

local_dataset_path='/data/Dataset_all_random'
single_img_folder='/home/eva/space_center/moon_8K/Single_Image/'

echo 'Start checking original dataset'

#for i in $(seq 0 9)
#for i in $(seq 0 )
#do
#  for j in $(seq 0 9)
#  do
#    for img in $(ls "${local_dataset_path}/$i/${i}_$j/")
#    do
#      pngcheck -q "${local_dataset_path}/$i/${i}_$j/$img"
#      retval=$?
#      if [ $retval -ne 0 ]; then
#        echo $retval
#      fi
##      python generate_single_image.py -s $img
#
#    done
#  done
#done
#
#echo 'End checking original dataset'

pngcheck -q "${local_dataset_path}/5/5_0/Dataset_all_random_50377.png"
retval=$?
if [ $retval -ne 0 ]; then
  echo $retval
fi