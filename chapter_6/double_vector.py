import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

source = numpy.random.randn(1000)
source = source.astype(numpy.float32)
source_gpu_ptr = cuda.to_device(source.tobytes())

result = numpy.empty_like(source)
result_gpu_ptr = cuda.to_device(result.tobytes())

mod = SourceModule("""
__global__ void doubleVector(float *input, float *output)
{
    int i = threadIdx.x;
    output[i] = pow(input[i], 20);
}
""")

func = mod.get_function("doubleVector")
func(source_gpu_ptr, result_gpu_ptr, block=(1000, 1, 1))

result = cuda.from_device_like(result_gpu_ptr, result)

print("ORIGINAL MATRIX")
print(source)

print("RESULT")
print(result)
