import logging
import multiprocessing
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def foo():
    name = multiprocessing.current_process().name
    logging.info('Process {} started'.format(name))
    time.sleep(20)
    logging.info('Process {} finished'.format(name))


def main():
    bg = multiprocessing.Process(name='background', target=foo)
    bg.daemon = True

    simple = multiprocessing.Process(name='simple', target=foo)
    simple.daemon = False

    bg.start()
    simple.start()


if __name__ == "__main__":
    main()
