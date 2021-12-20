import numpy as np
from mpi4py import MPI

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
neighbour_processes = [0, 0, 0, 0]

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    grid_rows = int(np.floor(np.sqrt(comm.size)))
    grid_column = grid_rows

    if rank == 0:
        print("Building a {}x{} grid topology".format(grid_rows, grid_column))

    cartesian_communicator = comm.Create_cart((grid_rows, grid_column),
                                              periods=(False, False),
                                              reorder=True)

    my_mpi_row, my_mpi_col = cartesian_communicator.Get_coords(cartesian_communicator.rank)

    neighbour_processes[UP], neighbour_processes[DOWN] = cartesian_communicator.Shift(0, 1)
    neighbour_processes[LEFT], neighbour_processes[RIGHT] = cartesian_communicator.Shift(1, 1)

    print("""
        Process: {}
            Row:                        {}
            Column:                     {}
            neighbour_processes[UP]     {}
            neighbour_processes[DOWN]   {}
            neighbour_processes[LEFT]   {}
            neighbour_processes[RIGHT]  {}
    """.format(rank, my_mpi_row, my_mpi_col,
               neighbour_processes[UP],
               neighbour_processes[DOWN],
               neighbour_processes[LEFT],
               neighbour_processes[RIGHT]))
