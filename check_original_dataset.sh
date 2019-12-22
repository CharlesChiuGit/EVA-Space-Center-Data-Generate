#!/bin/bash

local_dataset_path='/data/Dataset_all_random'
single_img_folder='/home/eva/space_center/moon_8K/Single_Image/'
object="Moon_8K.obj"

git pull
echo 'Start checking original dataset'
rm "../generate_single_image.py"
cp "generate_single_image.py" "../"
rm "../config.py"
cp "config.py" "../"

for i in $(seq 0 9)
do
  for j in $(seq 0 9)
  do
    for img in "${local_dataset_path}/$i/${i}_$j"/*.png
    do
      pngcheck -q "${img}"
      retval=$?
      if [ $retval -ne 0 ]; then
        OIFS="$IFS"
        IFS='/'
        read -r -a new_string <<< "${img}"
        IFS="$OIFS"
        cd "../" && python "generate_single_image.py" "${object}" "${new_string[5]}"
        cp "${img}" "${single_img_folder}/defect_image"
        cp "${local_dataset_path}/target_$i.json" "${single_img_folder}/defect_image/target_${i}_${new_string[5]}.json"
        cp "${single_img_folder}/${new_string[5]}" "${img}"
        cd "EVA-Space-Center-Data-Generate" && python "replace_target.py" "${new_string[5]}" "$i"
      fi
    done
  done
done
echo 'End checking original dataset'

#echo 'End checking original dataset'
#
#img="Dataset_all_random_50377.png"
#pngcheck -q "${local_dataset_path}/5/5_0/${img}"
#retval=$?
#if [ $retval -ne 0 ]; then
#  echo "${img}"
#fi