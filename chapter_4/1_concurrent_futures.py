# Sequence execution in 2.046816 seconds
# Thread pool execution in 1.6185779999999999 seconds
# Process pool execution in 0.011490999999999918 seconds

import concurrent.futures
import time

number_list = range(10)


def evaluate_item(x):
    result_item = count(x)
    print("Item {} result: {}".format(x, result_item))


def count(number):
    i = 0
    for i in range(1000000):
        i = i + 1
    return i*number


if __name__ == '__main__':
    start_time = time.clock()
    for item in number_list:
        evaluate_item(item)
    print("Sequence execution in {} seconds".format(time.clock() - start_time))

    start_time = time.clock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for item in number_list:
            executor.submit(evaluate_item, item)
            print("Task {} completed".format(item))
    print("Thread pool execution in {} seconds".format(time.clock() - start_time))

    start_time = time.clock()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        for item in number_list:
            executor.submit(evaluate_item, item)
            print("Task {} completed".format(item))
    print("Process pool execution in {} seconds".format(time.clock() - start_time))


