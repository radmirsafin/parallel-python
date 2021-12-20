import logging
import threading
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def first_function():
    thread_name = threading.current_thread().getName()
    logging.info('{} is starting'.format(thread_name))
    time.sleep(2)
    logging.info('{} is exiting'.format(thread_name))


def second_function():
    thread_name = threading.current_thread().getName()
    logging.info('{} is starting'.format(thread_name))
    time.sleep(2)
    logging.info('{} is exiting'.format(thread_name))


def third_function():
    thread_name = threading.current_thread().getName()
    logging.info('{} is starting'.format(thread_name))
    time.sleep(2)
    logging.info('{} is exiting'.format(thread_name))


def main():
    threads = []

    for i in ['first', 'second', 'third']:
        threads.append(threading.Thread(name='{}_function'.format(i), target=first_function))

    for th in threads:
        th.start()

    for th in threads:
        th.join()


if __name__ == "__main__":
    main()
