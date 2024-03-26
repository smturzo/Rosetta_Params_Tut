#!/bin/sh
#SBATCH --job-name=debug_games_inp
#SBATCH --time=15:00:00
#SBATCH --ntasks-per-node=4
#SBATCH --error=./outputs/test_error.txt
#SBATCH --output=./outputs/test_log.txt
#SBATCH --mail-user=bturzo@flatironinstitute.org
#SBATCH --mail-type=END,FAIL
#SBATCH --partition=ccb --constraint=skylake --export=ALL
set -vx

/mnt/home/vmulligan/GAMESS/gamess_openmp_2022_02/rungms Test_Molecule.inp 00 4 >& ../outputs/test_molecule.gamout 
