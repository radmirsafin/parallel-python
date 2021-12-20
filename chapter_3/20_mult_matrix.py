#   200x200
#
#       2 Processes
#           1:      6.42 seconds
#           2:      6.33 seconds
#           3:      6.68 seconds
#           avg:    6.47 seconds
#
#       4 Processes
#           1:      4.22 seconds
#           2:      4.36 seconds
#           3:      4.62 seconds
#           avg:    4.40 seconds
#
#       8 Processes
#           1:      4.50 seconds
#           2:      4.64 seconds
#           3:      4.79 seconds
#           avg:    4.64 seconds
#
#       16 Processes
#           1:      5.05 seconds
#           2:      4.84 seconds
#           3:      6.54 seconds
#           avg:    5.47 seconds

from mpi4py import MPI
import numpy
import time


def execute_task(task, matrix_a, matrix_b):
    row_num = task[0]
    column_num = task[1]
    row = matrix_a[row_num]
    column = [rw[column_num] for rw in matrix_b]
    result = 0
    for i in range(len(row)):
        result += row[i] * column[i]
    return result


def create_tasks(matrix_a, matrix_b, process_count):
    task_list = []
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            task_list.append((i, j))
    return split_tasks(task_list, process_count)


def split_tasks(task_list, process_count):
    task_list_parts = []

    for _ in range(process_count):
        task_list_parts.append([])

    curr_number = 0
    for t in task_list:
        task_list_parts[curr_number].append(t)
        curr_number += 1
        if curr_number == process_count:
            curr_number = 0
    return task_list_parts


def join_results(all_process_results):
    res = []
    for r in all_process_results:
        res += r
    return res


if __name__ == '__main__':

    L = 200
    M = 200
    N = 200
    # L x M
    matrixA = numpy.random.randint(10, size=(L, M))
    # M x N
    matrixB = numpy.random.randint(10, size=(M, N))
    # L x N
    matrixC = numpy.zeros((L, N), dtype=numpy.int)

    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    if rank == 0:
        start_time = time.time()
        tasks = create_tasks(matrixA, matrixB, size)
    else:
        start_time = None
        tasks = None

    my_tasks = comm.scatter(tasks, root=0)
    my_results = []

    for my_task in my_tasks:
        temp_result = (*my_task, execute_task(my_task, matrixA, matrixB))
        my_results.append(temp_result)

    results = comm.gather(my_results, root=0)

    if rank == 0:
        results = join_results(results)
        for item in results:
            matrixC[item[0]][item[1]] = item[2]
        print(matrixC)
        print("------- %s seconds -------" % (time.time() - start_time))
