import multiprocessing


def set_item(dictionary, key, value):
    dictionary[key] = value


def main():
    manager = multiprocessing.Manager()
    dictionary = manager.dict()

    jobs = []
    for i in range(10):
        jobs.append(multiprocessing.Process(target=set_item, args=(dictionary, i, i*2)))

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

    print('Result: {}'.format(dictionary))


if __name__ == "__main__":
    main()
