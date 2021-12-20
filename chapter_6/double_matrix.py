import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

source = numpy.random.randn(32, 32)
source = source.astype(numpy.float32)
source_gpu_ptr = cuda.to_device(source.tobytes())

result = numpy.empty_like(source)
result_gpu_ptr = cuda.to_device(result.tobytes())

mod = SourceModule("""
__global__ void doubleMatrix(float input[32][32], float output[32][32])
{
    int i = threadIdx.x;
    int j = threadIdx.y;
    output[i][j] = pow(input[i][j], 2);
}
""")

func = mod.get_function("doubleMatrix")

func(source_gpu_ptr, result_gpu_ptr, block=(32, 32, 1))
result = cuda.from_device_like(result_gpu_ptr, result)

print("ORIGINAL MATRIX")
print(source)

print("RESULT")
print(result)
