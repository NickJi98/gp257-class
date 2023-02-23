#!/usr/bin/env python3

from mpi4py import MPI
import numpy as np
import argparse
import time


def create_parser():
    ''' Create parser for inputs '''

    parser = argparse.ArgumentParser(description='MPI Matrix Multiplication')
    parser.add_argument('N', type=int,
                        help='Size of square matrices')
    parser.add_argument('--dtype', type=str, default='float64',
                        choices=['float64', 'float32'],
                        help='Float data type')
    return parser


# Read matrix size and data type
parser = create_parser()
args = parser.parse_args()
dtype_dict = {'float32': np.float32, 'float64': np.float64}

N = args.N
dtype = dtype_dict[args.dtype]

# MPI init
comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nproc = comm.Get_size()

if my_rank == 0:
    print('Start MPI', time.strftime("%H:%M:%S", time.localtime()))

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

if my_rank == 0:
    print('Finish creating communicators', time.strftime("%H:%M:%S", time.localtime()))

# Create empty matrix for row and column blocks
row_block = np.empty((Nsub, N), dtype=dtype)
col_block = np.empty((N, Nsub), dtype=dtype)

# Broadcast row-block of matrix A
if my_col == 0:
    row_block = np.random.rand(Nsub, N).astype(dtype)
row_comm.Bcast(row_block, root=0)

# Broadcast column-block of matrix B
if my_row == 0:
    col_block = np.random.rand(N, Nsub).astype(dtype)
col_comm.Bcast(col_block, root=0)

if my_rank == 0:
    print('Finish broadcasting', time.strftime("%H:%M:%S", time.localtime()))

# Block matrix multiplication
my_block = np.dot(row_block, col_block)

if my_rank == 0:
    print('Finish block multiplication', time.strftime("%H:%M:%S", time.localtime()))

# Gather result matrix C
# Gather in the row direction
res_mat_row = None
if my_col == 0:
    res_mat_row = np.empty((nblock, Nsub, Nsub), dtype=dtype)
row_comm.Gather(my_block, res_mat_row, root=0)

# Gather in the column direction
if my_rank == 0:
    res_mat = np.empty((nblock, nblock, Nsub, Nsub), dtype=dtype)
    res_mat[0] = res_mat_row
    for i in range(1, nblock):
        col_comm.Recv(res_mat[i], source=i)
elif my_col == 0:
    col_comm.Send(res_mat_row, dest=0)

if my_rank == 0:
    res_mat = np.hstack(np.hstack(res_mat))
    print('Shape of result matrix:', res_mat.shape)
    print('Finish gathering', time.strftime("%H:%M:%S", time.localtime()))

MPI.Finalize()
