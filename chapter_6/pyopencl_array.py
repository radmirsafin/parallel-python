import numpy as np
import pyopencl as cl
from timeit import default_timer as timer
from jinja2 import Template

array_size = 5000
diagonal_count = array_size * 2 - 1

source_array = np.random.randn(array_size, array_size).astype(np.float32)
result_array = np.empty(shape=diagonal_count).astype(np.float32)

platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)
mf = cl.mem_flags

source_array_gpu_ptr = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=source_array)

kernel_code = Template("""
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
""").render(array_size=array_size)

program = cl.Program(context, kernel_code).build()

result_array_gpu_ptr = cl.Buffer(context, mf.WRITE_ONLY, result_array.nbytes)

start_time = timer()
program.sumDiagonal(queue, (diagonal_count, 1), None, source_array_gpu_ptr, result_array_gpu_ptr)
gpu_time = timer() - start_time

cl.enqueue_copy(queue, result_array, result_array_gpu_ptr)

print("Time: ", gpu_time)
print(source_array.sum(), result_array.sum())
