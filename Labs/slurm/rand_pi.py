#!/usr/bin/env python3
import numpy as np
import os

# Seed based on slurm task id
task_id = int(os.getenv('SLURM_ARRAY_TASK_ID'))
np.random.seed(task_id)

# Total number of points (correspond to significant digits of the estimation)
N = 10000000

# Generate random numbers between 0 and 1
x = np.random.rand(N)
y = np.random.rand(N)

# Estimate pi
est_pi = 4 * np.sum((x**2 + y**2) <= 1) / N

# Return sum of squares
f = open("est_%d.txt" %(task_id), "w")
f.write('%s' %(est_pi))
f.close()
