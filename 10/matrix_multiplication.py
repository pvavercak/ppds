#!/usr/bin/env python3
import numpy
import math
from numba import cuda


@cuda.jit
def matmul(A, B, C):
    row, col = cuda.grid(2)
    if row < C.shape[0] and col < C.shape[1]:
        tmp = 0.
        for k in range(A.shape[1]):
            tmp += A[row, k] * B[k, col]
        C[row][col] = tmp


rows_a = 24
cols_a = 12
cols_b = 22

A = numpy.full((rows_a, cols_a), 3, numpy.float32)
B = numpy.full((cols_a, cols_b), 4, numpy.float32)

A_device = cuda.to_device(A)
B_device = cuda.to_device(B)

C_device = cuda.device_array((rows_a, cols_b))

threads_per_block = (16, 16)

block_x = math.ceil(A.shape[0] / threads_per_block[0])
block_y = math.ceil(B.shape[1] / threads_per_block[1])

matmul[(block_x, block_y), threads_per_block](A_device, B_device, C_device)

C = C_device.copy_to_host()

print(C)
