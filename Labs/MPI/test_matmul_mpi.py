#!/usr/bin/env python3

from mpi4py import MPI
import numpy as np

# Read matrix size and data type
N = 32
dtype = np.float64

# MPI init
comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nproc = comm.Get_size()

# Number of blocks per side
nblock = np.sqrt(nproc)
if np.mod(nblock, 1) != 0:
    msg = 'Number of processor M should be a perfect square number!'
    raise Exception(msg)
else:
    nblock = nblock.astype('int')

# Size of each block
if np.mod(N/nblock, 2) != 0:
    msg = 'Number of processor M should satisfy that ' \
          'matrix size N is evenly divisible by sqrt(M)!'
    raise Exception(msg)
else:
    Nsub = (N / nblock).astype('int')

# Create Cartesian grid
cart2d = comm.Create_cart(dims=[nblock, nblock])
[my_row, my_col] = cart2d.Get_coords(my_rank)

# Sub-communicator (each row & column)
row_comm = cart2d.Sub(remain_dims=[False, True])
col_comm = cart2d.Sub(remain_dims=[True, False])

# Create empty matrix for row and column blocks
row_block = np.empty((Nsub, N))
col_block = np.empty((N, Nsub))

# Broadcast row-block of matrix A
if my_col == 0:
    row_block = np.random.rand(Nsub, N).astype(dtype)
row_comm.Bcast(row_block, root=0)

# Broadcast column-block of matrix B
if my_row == 0:
    col_block = np.random.rand(N, Nsub).astype(dtype)
col_comm.Bcast(col_block, root=0)

# Block matrix multiplication
my_block = np.dot(row_block, col_block)

# Gather result matrix C
res_mat_row = row_comm.gather(my_block, root=0)
res_mat = col_comm.gather(res_mat_row, root=0)

# Gather matrices A and B
A_mat = col_comm.gather(row_block, root=0)
B_mat = row_comm.gather(col_block, root=0)

# Test with np.dot()
if my_rank == 0:
    res_mat = np.block(np.block(res_mat))
    A_mat = np.vstack(A_mat)
    B_mat = np.hstack(B_mat)

    np_mat = np.dot(A_mat, B_mat)
    err = np.sum(res_mat - np_mat)
    print(res_mat)
    assert err == 0, 'Result not correct: Element error is %s' % err

MPI.Finalize()
