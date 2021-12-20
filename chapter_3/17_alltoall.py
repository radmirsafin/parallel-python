from mpi4py import MPI
import numpy
import random

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

a_size = 1
send_data = (random.randint(100, 199))*numpy.arange(size, dtype=int)
recv_data = numpy.empty(size*a_size, dtype=int)
comm.Alltoall(send_data, recv_data)

print("Process {} sending {} receiving {}"
      .format(rank, send_data, recv_data))


