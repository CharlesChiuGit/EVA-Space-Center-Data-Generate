#!/bin/bash

dataset_name='Dataset_test_1'
total_number=10
lv1_index=2
lv2_index=2
local_dataset_path="/data/${dataset_name}"
regen_img_folder="$HOME/space_center/moon_8K/Regen_Image/"
object="Moon_8K.obj"
git_folder="$HOME/space_center/moon_8K/EVA-Space-Center-Data-Generate"
git pull
# ----------------------------------------------
#rm "../config.py"
cp "config.py"  ".."
cp "generate_dataset.py"  ".."
cp "generate_single_image.py" ".."
# ----------------------------------------------

echo 'Start creating original dataset'
cd "$HOME/space_center/moon_8K/" && python "generate_dataset.py" -o "${object}" -dn "${dataset_name}" -n "${total_number}" -lv1 "${lv1_index}" -lv2 "${lv2_index}"
echo 'End creating original dataset'
# ----------------------------------------------

echo "Start checking original dataset ${dataset_name}"
lv1_dummy="$(${lv1_index} - 1)"
echo "${lv1_dummy}"
lv2_dummy="$(${lv2_index} - 1)"
echo "${lv2_dummy}"
for i in $(seq 0 "${lv1_dummy}")
do
  echo "${i}"
  for j in $(seq 0 "${lv2_dummy}")
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
        python "generate_single_image.py" -o "${object}" -d "${new_string[5]}"
        cp "${img}" "${regen_img_folder}/defect_image"
        cp "${local_dataset_path}/target_$i.json" "${regen_img_folder}/defect_image/target_${i}_${new_string[5]}.json"
        cp "${regen_img_folder}/${new_string[5]}" "${img}"
        cd "${git_folder}" && python "replace_target.py" -d "${new_string[5]}" -i "$i" -o "${object}" -dn "${dataset_name}" -n "${total_number}" -lv1 "${lv1_index}" -lv2 "${lv2_index}"
      fi
    done
  done
done
cd "${git_folder}" && python "compress_file.py" -dn "${dataset_name}" -n "${total_number}" -lv1 "${lv1_index}" -lv2 "${lv2_index}"
echo 'End checking original dataset'

#echo 'End checking original dataset'
#
#img="Dataset_all_random_50377.png"
#pngcheck -q "${local_dataset_path}/5/5_0/${img}"
#retval=$?
#if [ $retval -ne 0 ]; then
#  echo "${img}"
#fi