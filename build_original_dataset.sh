#!/bin/bash

dataset_name='Dataset_test_new'
total_number=100
lv1_index=10
lv2_index=10
local_dataset_path="/data/${dataset_name}"
object="Moon_8K.obj"
git_folder="$HOME/space_center/moon_8K/EVA-Space-Center-Data-Generate"
# ----------------------------------------------

conda_dir="$HOME/anaconda2/etc/profile.d"
# shellcheck source=/dev/null
source "${conda_dir}/conda.sh"
conda activate "space"
cd "${git_folder}" && git pull
# ----------------------------------------------

cp "config.py"  ".."
cp "generate_dataset.py"  ".."
cp "regenerate_defect_image.py" ".."
# ----------------------------------------------

echo 'Start creating original dataset'
cd "$HOME/space_center/moon_8K/" && python "generate_dataset.py" -o "${object}" -dn "${dataset_name}" -n "${total_number}" -lv1 "${lv1_index}" -lv2 "${lv2_index}"
echo 'End creating original dataset'
# ----------------------------------------------
# Define function
regenerate_defect_image(){
  defect_image=$1
  target_index=$2
  echo "${defect_image}"
  cd "$HOME/space_center/moon_8K/" && python "regenerate_defect_image.py" -d "${defect_image}" -i "${target_index}" -dn "${dataset_name}"
}

# ----------------------------------------------

echo "Start checking original dataset ${dataset_name}"

for i in $(seq 0 "$((lv1_index - 1))")
do
  echo "${i}"
  for j in $(seq 0 "$((lv2_index - 1))")
  do
    for img in "${local_dataset_path}/$i/${i}_$j"/*.png
    do
      echo "${img}"
      pngcheck -q "${img}"
      retval=$?
      if [ $retval -ne 0 ]; then
        regenerate_defect_image "${img}" "$i"
      fi
    done
  done
done
cd "${git_folder}" && python "compress_file.py" -dn "${dataset_name}" -lv1 "${lv1_index}" -lv2 "${lv2_index}"
echo 'End checking original dataset'
# ----------------------------------------------

# build remote dataset after creat original dataset
local_private_key="$HOME/.ssh/eva_59"
remote_IP='charleschiu@140.113.86.58'
ssh -i "${local_private_key}" "${remote_IP}" bash << "EOF"
  git_folder="$HOME/EVA-Space-Center-Data-Generate"
  remote_script="build_local_dataset.sh"
  cd "${git_folder}"
  git pull
  bash ${remote_script} ${dataset_name} ${lv1_index} ${lv2_index}
  exit
EOF