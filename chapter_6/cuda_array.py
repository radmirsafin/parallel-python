import numpy as np
from timeit import default_timer as timer
import math
from jinja2 import Template
from pycuda import compiler, driver, autoinit

array_size = 5000
diagonal_count = array_size * 2 - 1

source_array = np.random.randn(array_size, array_size).astype(np.float32)
result_array = np.zeros(shape=diagonal_count).astype(np.float32)

block = (32, 32, 1)
grid = (math.ceil(diagonal_count / 1024), 1)

kernel_code = Template("""
__global__ void kernel(float *input, float *output) {

    int threadsPerBlock  = blockDim.x * blockDim.y;
    int threadNumInBlock = threadIdx.x + blockDim.x * threadIdx.y;
    int blockNumInGrid   = blockIdx.x  + gridDim.x  * blockIdx.y;
    int index = blockNumInGrid * threadsPerBlock + threadNumInBlock;
    
    int startPosI = 0;
    int startPosJ = 0;

    int shift = {{array_size}} - index - 1;

    if (shift > 0) {
        startPosI = shift; 
    }
    else {
        startPosJ = -shift;
    }

    float sum = 0;

    for (int i = startPosI, j = startPosJ; i < {{array_size}} && j < {{array_size}}; i++, j++) {
        sum += input[i * {{array_size}} + j];
    }

    if (startPosI < {{array_size}} && startPosJ < {{array_size}}) {
        output[index] = sum;
    }
}
""").render(array_size=array_size)

mod = compiler.SourceModule(kernel_code, options=['--compiler-options', '-Wall'])
func = mod.get_function("kernel")

source_array_gpu_ptr = driver.to_device(source_array.tobytes())
result_array_gpu_ptr = driver.to_device(result_array.tobytes())

start_time = timer()
func(
    source_array_gpu_ptr,
    result_array_gpu_ptr,
    grid=grid,
    block=block,
)
gpu_time = timer() - start_time

result_array = driver.from_device_like(result_array_gpu_ptr, result_array)

print("Time: ", gpu_time)
print(source_array.sum(), result_array.sum())
