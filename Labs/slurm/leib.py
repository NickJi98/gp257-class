#!/usr/bin/env python3
import numpy as np

# Calculate Pi with Leibniz formula
N = 1000000
leib_series = np.array([(-1)**k / (2*k+1) for k in range(N)])
res = np.sum(leib_series) * 4

f = open("result1.txt", "w")
f.write('%s' %res)
f.close()
