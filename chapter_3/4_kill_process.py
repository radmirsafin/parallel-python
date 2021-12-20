import logging
import multiprocessing
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def foo():
    name = multiprocessing.current_process().name
    logging.info('Process {} started'.format(name))
    time.sleep(200)
    logging.info('Process {} finished'.format(name))


def main():
    p = multiprocessing.Process(name='background', target=foo)
    logging.info('Process before execution: {} {}'.format(p, p.is_alive()))
    p.start()
    logging.info('Process running: {} {}'.format(p, p.is_alive()))
    time.sleep(10)
    p.terminate()
    logging.info('Process terminated: {} {}'.format(p, p.is_alive()))
    p.join()
    logging.info('Process joined: {} {}'.format(p, p.is_alive()))
    logging.info('Process exit with code: {}'.format(p.exitcode))
    time.sleep(10)


if __name__ == "__main__":
    main()
