#!/usr/bin/env python3

from mpi4py import MPI
import numpy as np

# Read matrix size and data type
N = 1024
dtype = np.float32

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

# Block matrix multiplication
my_block = np.dot(row_block, col_block)

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

# Gather matrices A and B
if my_rank == 0:
    A_mat = np.empty((nblock, Nsub, N), dtype=dtype)
    B_mat = np.empty((nblock, N, Nsub), dtype=dtype)

    A_mat[0] = row_block
    B_mat[0] = col_block

    for i in range(1, nblock):
        col_comm.Recv(A_mat[i], source=i)
        row_comm.Recv(B_mat[i], source=i)

else:
    if my_col == 0:
        col_comm.Send(row_block, dest=0)
    if my_row == 0:
        row_comm.Send(col_block, dest=0)

# Test with np.dot()
if my_rank == 0:
    res_mat = np.hstack(np.hstack(res_mat))
    A_mat = np.vstack(A_mat)
    B_mat = np.hstack(B_mat)

    np_mat = np.dot(A_mat, B_mat)
    err = np.mean(np.abs(res_mat-np_mat)/np_mat)

    print('Test with matrix size N = %d' % N)
    print('Showing random 10 entries from the matrix ...\n')
    row_inds = np.random.randint(0, N, size=(10,))
    col_inds = np.random.randint(0, N, size=(10,))
    print('My result with type: %s' % res_mat.dtype)
    print(res_mat[row_inds, col_inds])
    print()
    print('Numpy result with type: %s' % np_mat.dtype)
    print(np_mat[row_inds, col_inds])
    assert err < 2 * np.finfo(dtype).eps, \
        'Result not correct: Element-wise relative error is %s' % err

MPI.Finalize()
