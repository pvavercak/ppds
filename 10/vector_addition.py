import numpy
import math
from numba import cuda


@cuda.jit
def vector_add(vec, add):
    tid = cuda.grid(1)
    if vec.size > tid:
        vec[tid] += add


add = 5
vec = numpy.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

vec_device = cuda.to_device(vec)

vector_add[1, 32](vec_device, add)

print(vec_device.copy_to_host())
