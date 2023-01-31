#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --partition=debug
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=1GB
#SBATCH --cpus-per-task=1
#SBATCH --dependency=afterok:5531

echo "Computing is started at $(date)."
spack load python@3.10.8
python3 ./mean_pi.py
rm -f slurm-5531*.out
echo "Computing is stopped at $(date)."
