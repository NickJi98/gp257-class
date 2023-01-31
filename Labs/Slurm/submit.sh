#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --partition=debug
#SBATCH --time=2:00:00
#SBATCH --mem=2GB
#SBATCH --cpus-per-task=1

echo "Computing is started at $(date)."
spack load python@3.10.8
python3 ./leib.py
echo "Computing is stopped at $(date)."
