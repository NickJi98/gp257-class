#!/bin/bash

#SBATCH --ntasks=4
#SBATCH --ntasks-per-node=4
#SBATCH --partition=preempt
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH -o test_N20480_M4_F32.out
#SBATCH --threads-per-core=1
#SBATCH --time=00:30:00

#****************************************************#
# Author:
# Thomas Cullison, Stanford University, 2023
#



##*****************************************##
## size of N for N*N matrix
MATSIZE=20480
DTYPE='float32'


##*****************************************##
## Header Info
echo;
echo "Starting sbatch script";
echo "Job ID: $SLURM_JOB_ID";
echo "DATE: $(date), NTASKS: $SLURM_NTASKS, NNODES: $SLURM_NNODES";
echo;


##*****************************************##
## SPACK setup (like modules)
echo ". /home/spack/spack/share/spack/setup-env.sh";
. /home/spack/spack/share/spack/setup-env.sh;
echo;
echo "spack load intel-oneapi-mpi";
spack load intel-oneapi-mpi;
echo "which mpiexec";
which mpiexec;
echo "spack load python@3.10.8";
spack load python@3.10.8;
echo "python --version";
python --version 2>&1;


##*****************************************##
## MPI
MY_MPI_MATMUL="matmul_mpi.py"
echo;
echo "Running MatMul";
echo "DATE: $(date)";
echo;
echo "mpiexec -n $SLURM_NTASKS python $MY_MPI_MATMUL $MATSIZE --dtype $DTYPE";
echo;
mpiexec -n $SLURM_NTASKS python $MY_MPI_MATMUL $MATSIZE --dtype $DTYPE;


##*****************************************##
## Footer Info
echo;
echo "Done...";
echo "DATE: $(date), NTASKS: $SLURM_NTASKS, NNODES: $SLURM_NNODES";
