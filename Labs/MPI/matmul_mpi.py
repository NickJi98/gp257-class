#!/usr/bin/env python3

from mpi4py import MPI
import numpy as np
import argparse


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

# Number of blocks per side
nblock = int(np.sqrt(nproc))
if np.mod(nblock, 1) != 0:
    msg = 'Number of processor M should be a perfect square number!'
    raise Exception(msg)

if np.mod(N/nblock, 2) != 0:
    msg = 'Number of processor M should satisfy that ' \
          'matrix size N is evenly divisible by sqrt(M)!'
    raise Exception(msg)

# Create Cartesian grid
cart2d = comm.Create_cart(dims=[nblock, nblock])
my_coord = cart2d.Get_coords(my_rank)

# Broadcast row-block of matrix A
if my_coord[1] == 0:
    row_block = np.random.rand(nblock, N).astype(dtype)
    for pid_col in range(1, nblock):
        comm.send(row_block, dest=cart2d.Get_cart_rank([my_coord[0], pid_col]))

else:
    row_block = comm.recv(source=cart2d.Get_cart_rank([my_coord[0], 0]))


# Broadcast column-block of matrix B
if my_coord[0] == 0:
    col_block = np.random.rand(N, nblock).astype(dtype)
    for pid_row in range(1, nblock):
        comm.send(col_block, dest=cart2d.Get_cart_rank([pid_row, my_coord[1]]))

else:
    col_block = comm.recv(source=cart2d.Get_cart_rank([0, my_coord[1]]))

# Block matrix multiplication
my_block = np.dot(row_block, col_block)

# Gather data
if my_rank != 0:
    comm.send(my_block, dest=0)

if my_rank == 0:
    res_mat = np.zeros((N, N), dtype=dtype)
    res_mat[:nblock, :nblock] = my_block
    for pid in range(1, nproc):
        cur_block = comm.recv(source=pid)
        pid_row, pid_col = cart2d.Get_coords(pid)
        res_mat[pid_row*nblock:(pid_row+1)*nblock,
                pid_col*nblock:(pid_col+1)*nblock] = cur_block

    np.savez('my_res.npz', C=res_mat)

MPI.Finalize()
