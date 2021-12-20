import math
from random import random
from scoop import futures
from time import time


def evaluate_number_of_points_in_unit_circle(attempts):
    points_fallen_in_unit_disks = 0
    for _ in range(0, attempts):
        x = random()
        y = random()
        radius = math.sqrt(x*x + y*y)
        if radius < 1:
            points_fallen_in_unit_disks = points_fallen_in_unit_disks + 1
    return points_fallen_in_unit_disks


def pi_calculus_with_montecarlo_method(workers, attempts):
    print("Number of workers {} - number of attempts {}".format(workers, attempts))
    bt = time()
    evaluate_tasks = futures.map(evaluate_number_of_points_in_unit_circle, [attempts] * workers)
    task_results = sum(evaluate_tasks)
    print("{} points fallen in a unit disk after ".format(task_results/attempts))
    pi_value = (4. * task_results / float(workers * attempts))
    comp_time = time() - bt
    print("Value if pi = {}".format(pi_value))
    print("Error percentage = {}".format(((abs(pi_value - math.pi) * 100) / math.pi)))
    print("Total time: {}".format(comp_time))


if __name__ == '__main__':
    for i in range(1, 4):
        pi_calculus_with_montecarlo_method(i*1000, i*1000)
        print(" ")
