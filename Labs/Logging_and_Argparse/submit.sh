#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --partition=cpu
#SBATCH --time=1:00:00
#SBATCH --mem=16GB
#SBATCH --cpus-per-task=1

expr='file3/(file1+file2)*file4'
outfile='out.npz'
infile='labVec0.npz labVec1.npz labVec2.npz labVec3.npz'

echo "Computing is started at $(date)."
spack load python@3.10.8
python3 ./npz_calc.py ${expr} --outfile ${outfile} --infile ${infile}
echo "Computing is stopped at $(date)."
