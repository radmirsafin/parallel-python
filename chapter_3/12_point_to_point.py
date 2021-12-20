from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
print("my rank is: {}".format(rank))

if rank == 0:
    data1 = 10000000
    destination_process = 4
    comm.send(data1, dest=destination_process)
    print("sending data {} to process {}".format(data1, destination_process))

if rank == 1:
    destination_process1 = 8
    data2 = "hello"
    comm.send(data2, destination_process1)
    print("sending data {} to process {}".format(data2, destination_process1))

if rank == 4:
    data3 = comm.recv(source=0)
    print("data received is = {}".format(data3))

if rank == 8:
    data4 = comm.recv(source=1)
    print("data1 received is = {}".format(data4))


