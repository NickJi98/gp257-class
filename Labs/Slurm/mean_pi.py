#!/usr/bin/env python3
import numpy as np
import glob

# All estimations of pi
file_list = glob.glob('./est_*.txt')
Nfile = len(file_list)

# Average estimation of pi
est_pi = 0.0

for fname in file_list:
    file = open(fname, 'r')
    est_pi += float(file.read())

# Final estimation of pi
est_pi /= Nfile
f = open('result2.txt', 'w')
f.write('%s' %(est_pi))
f.close()
