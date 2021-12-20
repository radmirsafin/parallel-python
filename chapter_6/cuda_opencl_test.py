import pyopencl as cl
import numpy as np
from timeit import default_timer as timer
import math
from jinja2 import Template
from pycuda import compiler, driver, autoinit
import matplotlib.pyplot as plt

opencl_kernel_code = """
    __kernel void sumDiagonal(__global const float *input,  __global float *output) {

        int index = get_global_id(0);

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
"""

cuda_kernel_code = """
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
"""


def calculate_by_opencl(array_size, diagonal_count, source_array, result_array):
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)
    mf = cl.mem_flags

    source_array_gpu_ptr = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=source_array)
    kernel_code = Template(opencl_kernel_code).render(array_size=array_size)
    program = cl.Program(context, kernel_code).build()
    result_array_gpu_ptr = cl.Buffer(context, mf.WRITE_ONLY, result_array.nbytes)

    start_time = timer()
    program.sumDiagonal(queue, (diagonal_count, 1), None, source_array_gpu_ptr, result_array_gpu_ptr)
    gpu_time = timer() - start_time

    cl.enqueue_copy(queue, result_array, result_array_gpu_ptr)
    #
    # print("Time: ", gpu_time)
    # print(source_array.sum(), result_array.sum())
    return gpu_time


def calculate_by_cuda(array_size, diagonal_count, source_array, result_array):
    block = (32, 32, 1)
    grid = (math.ceil(diagonal_count / 1024), 1)

    kernel_code = Template(cuda_kernel_code).render(array_size=array_size)

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

    # result_array = driver.from_device_like(result_array_gpu_ptr, result_array)
    # print("Time: ", gpu_time)
    # print(source_array.sum(), result_array.sum())
    return gpu_time


if __name__ == '__main__':
    array_sizes = []
    cuda_results = []
    opencl_results = []

    array_size = 500

    while (array_size <= 22000):
        array_sizes.append(array_size)
        diagonal_count = array_size * 2 - 1
        print("Array size: {}".format(array_size))

        source_array = np.random.randn(array_size, array_size).astype(np.float32)
        result_array = np.empty(shape=diagonal_count).astype(np.float32)

        cuda_time = calculate_by_cuda(array_size, diagonal_count, source_array, result_array)
        opencl_time = calculate_by_opencl(array_size, diagonal_count, source_array, result_array)

        #         print("Cuda time:   {:.6f}\nOpenCl time: {:.6f}\n===================".format(cuda_time, opencl_time))

        cuda_results.append(cuda_time)
        opencl_results.append(opencl_time)

        array_size += 500

    plt.plot(array_sizes, cuda_results, label="cuda")
    plt.plot(array_sizes, opencl_results, label="pyopencl")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()
