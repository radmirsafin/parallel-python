# python -m scoop -n 8 scoop_map.py

import operator
import time

from scoop import futures


def simulate_workload(input_data):
    time.sleep(0.01)
    return sum(input_data)


def compare_map_reduce():
    calc_list = list([a] * a for a in range(1000))

    map_scoop_time = time.time()
    res = futures.mapReduce(
        simulate_workload,
        operator.add,
        calc_list
    )
    map_scoop_time = time.time() - map_scoop_time
    print("futures.map in SCOOP executed in {0:.3f}s with result: {1}".format(
        map_scoop_time,
        res
    ))

    map_python_time = time.time()
    res = sum(map(simulate_workload, calc_list))
    map_python_time = time.time() - map_python_time
    print("map Python executed in: {0:.3f}s with result: {1}".format(
        map_python_time, res
    ))


if __name__ == '__main__':
    compare_map_reduce()
