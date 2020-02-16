#!/bin/bash

dataset_name='Dataset_test_7' # remember to change dataset_name and so on in EOF below
dataset_amount=1000
big_partition=10
small_partition=10
#local_dataset_path="/data/${dataset_name}"
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
cp "check_original_dataset.py" ".."
#cp "helper_function.py" ".."
# ----------------------------------------------

echo 'Start creating original dataset'
cd "$HOME/space_center/moon_8K/" || exit
python "generate_dataset.py" -dn "${dataset_name}" -n "${dataset_amount}" -bp "${big_partition}" -sp "${small_partition}"
echo 'End creating original dataset'
# ----------------------------------------------
# Define function
#regenerate_defect_image(){
#  defect_image=$1
#  target_index=$2
#  echo "${defect_image}"
#  cd "$HOME/space_center/moon_8K/" || exit
#  python "regenerate_defect_image.py" -d "${defect_image}" -ti "${target_index}" -dn "${dataset_name}"
#}

# ----------------------------------------------

echo "Start checking original dataset"
cd "$HOME/space_center/moon_8K/" || exit
python "check_original_dataset.py" -dn "${dataset_name}" -bp "${big_partition}" -sp "${small_partition}" -n "${dataset_amount}"
#for i in $(seq 0 "$((big_partition - 1))")
#do
#  echo "${i}"
#  for j in $(seq 0 "$((small_partition - 1))")
#  do
#    for img in "${local_dataset_path}/$i/${i}_$j"/*.png
#    do
##      echo "${img}"
#      pngcheck -v -q "${img}"
#      retval=$?
#      if [ $retval -ne 0 ]; then
#        regenerate_defect_image "${img}" "$i"
#      fi
#    done
#  done
#done
cd "${git_folder}" || exit
python "compress_file.py" -dn "${dataset_name}" -bp "${big_partition}" -sp "${small_partition}"
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
  dataset_name='Dataset_test_7'
  dataset_amount=1000
  big_partition=10
  small_partition=10
  bash ${remote_script} ${dataset_name} ${big_partition} ${small_partition} ${dataset_amount}
  exit
EOF