from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    array_to_share = [11, 22, 33, 44, 55, 66, 77, 88, 99, 100]
else:
    array_to_share = None

recvbuf = comm.scatter(array_to_share, root=0)

print("Process = {}, array_to_share = {}"
      .format(rank, recvbuf))

