import logging
import multiprocessing
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def foo():
    name = multiprocessing.current_process().name
    logging.info('Process {} started'.format(name))
    time.sleep(20)
    logging.info('Process {} ended'.format(name))


def main():
    main_process = multiprocessing.Process(name='main_process', target=foo)
    main_process.daemon = True

    sec_process = multiprocessing.Process(target=foo)

    main_process.start()
    sec_process.start()


if __name__ == "__main__":
    main()
