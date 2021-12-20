import logging
import multiprocessing
import datetime
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def with_barrier(synchronizer, serializer, sleep_time):
    time.sleep(sleep_time)

    name = multiprocessing.current_process().name

    synchronizer.wait()
    with serializer:
        logging.info('Process {} ---> {}'.format(name, datetime.datetime.now()))


def without_barrier(sleep_time):
    time.sleep(sleep_time)

    name = multiprocessing.current_process().name
    logging.info('Process {} ---> {}'.format(name, datetime.datetime.now()))


def main():
    synchronizer = multiprocessing.Barrier(2)
    serializer = multiprocessing.Lock()

    multiprocessing.Process(name='p1-with-barrier',
                            target=with_barrier,
                            args=(synchronizer, serializer, 2)).start()

    multiprocessing.Process(name='p2-with-barrier',
                            target=with_barrier,
                            args=(synchronizer, serializer, 1)).start()

    multiprocessing.Process(name='p3-without-barrier',
                            target=without_barrier,
                            args=(2,)).start()

    multiprocessing.Process(name='p4-without-barrier',
                            target=without_barrier,
                            args=(1,)).start()


if __name__ == "__main__":
    main()
