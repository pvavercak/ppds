import numpy
import math
from numba import cuda


@cuda.jit
def my_kernel(io_array):
    tx = cuda.threadIdx.x
    ty = cuda.blockIdx.x
    bw = cuda.blockDim.x
    pos = tx + ty * bw
    if pos < io_array.size:
        io_array[pos] *= 2


@cuda.jit
def my_kernel_simplified(io_array):
    pos = cuda.grid(1)
    if pos < io_array.size:
        io_array[pos] *= 2


@cuda.jit
def my_kernel_2D(io_array):
    x, y = cuda.grid(2)
    if x < io_array.shape[0] and y < io_array.shape[1]:
        io_array[x][y] *= 2


data_1D = numpy.ones(256)

threads_per_block_1D = 256

blocks_per_grid_1D = math.ceil(data_1D.shape[0] / threads_per_block_1D)

my_kernel[blocks_per_grid_1D, threads_per_block_1D](data_1D)
my_kernel_simplified[blocks_per_grid_1D, threads_per_block_1D](data_1D)

data_2D = numpy.ones((16, 16))

threads_per_block_2D = (16, 16)

blocks_per_grid_x = math.ceil(data_2D.shape[0] / threads_per_block_2D[0])
blocks_per_grid_y = math.ceil(data_2D.shape[1] / threads_per_block_2D[1])

blocks_per_grid_2D = (blocks_per_grid_x, blocks_per_grid_y)

my_kernel_2D[blocks_per_grid_2D, threads_per_block_2D](data_2D)

print(data_1D)

print(data_2D)
