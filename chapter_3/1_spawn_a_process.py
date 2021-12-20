import logging
import multiprocessing

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def foo(i):
    logging.info('Called function in process: {}'.format(i))


def main():
    process_jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=foo, args=(i,))
        process_jobs.append(p)
        p.daemon = True
        p.start()
        p.join()


if __name__ == "__main__":
    main()
