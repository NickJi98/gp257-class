#!/bin/bash

#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=16
#SBATCH --partition=normal
#SBATCH --nodes=4
#SBATCH -o N61440_M64_F32.out
#SBATCH --threads-per-core=1
#SBATCH --time=00:20:00
#SBATCH --mem=160GB

#****************************************************#
# Author:
# Thomas Cullison, Stanford University, 2023
#



##*****************************************##
## size of N for N*N matrix
MATSIZE=61440
DTYPE='float32'


##*****************************************##
## Header Info
echo;
echo "Starting sbatch script";
echo "Job ID: $SLURM_JOB_ID";
echo "DATE: $(date), NTASKS: $SLURM_NTASKS, NNODES: $SLURM_NNODES";
echo;


##*****************************************##
## Load modules
echo;
echo "module load openmpi/4.1.2";
module load openmpi/4.1.2;
echo "which mpiexec";
which mpiexec;
echo "module load python/3.9.0";
echo "module load py-numpy/1.20.3_py39";
echo "module load py-mpi4py/3.1.3_py39";
module load python/3.9.0;
module load py-numpy/1.20.3_py39;
module load py-mpi4py/3.1.3_py39;
echo "python --version";
python3 --version 2>&1;


##*****************************************##
## MPI
MY_MPI_MATMUL="matmul_mpi.py"
echo;
echo "Running MatMul";
echo "DATE: $(date)";
start_time=`date +%s`
echo;
echo "mpiexec -n $SLURM_NTASKS python $MY_MPI_MATMUL $MATSIZE --dtype $DTYPE";
echo;
mpiexec -n $SLURM_NTASKS python3 $MY_MPI_MATMUL $MATSIZE --dtype $DTYPE;


##*****************************************##
## Footer Info
echo;
echo "Done...";
end_time=`date +%s`
echo "DATE: $(date), NTASKS: $SLURM_NTASKS, NNODES: $SLURM_NNODES";
echo "Execution time: $(expr $end_time - $start_time) s";
