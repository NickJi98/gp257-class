#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --array=0-999
#SBATCH --partition=preempt
#SBATCH --time=0:10:00
#SBATCH --mem-per-cpu=1GB
#SBATCH --requeue

echo "Computing is started at $(date)."
spack load python@3.10.8
python3 ./rand_pi.py
echo "Computing is stopped at $(date)."
