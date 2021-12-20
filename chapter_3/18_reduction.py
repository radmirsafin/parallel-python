import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

array_size = 3
recvdata = np.zeros(array_size, dtype=np.int)
senddata = (rank+1)*np.arange(array_size, dtype=np.int)
print("Process {} sending {}".format(rank, senddata))

comm.Reduce(senddata, recvdata, root=0, op=MPI.SUM)
print("On task {} after reduce: {}".format(rank, recvdata))
