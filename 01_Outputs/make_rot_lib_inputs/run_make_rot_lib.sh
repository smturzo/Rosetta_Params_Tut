#!/bin/bash
#SBATCH --job-name=make_rot_lib_test
#SBATCH --time=05:00:00
#SBATCH --partition=ccb
#SBATCH --ntasks=20
#SBATCH --error=rotlib_error.txt
#SBATCH --output=rotlib_log.txt
#SBATCH --mail-user=bturzo@flatironinstitute.org
#SBATCH --mail-type=END,FAIL
set -vx
export PATH="/mnt/home/bturzo/ceph/Applications/Rosetta/source/bin:$PATH"
export PATH="/mnt/home/bturzo/ceph/Applications/Rosetta/source/database:$PATH"
MakeRotLib.linuxgccrelease -options_file HAL_rot_lib_main.txt -extra_res_fa ../HAL.params >& HAL_rot_lib.log 
