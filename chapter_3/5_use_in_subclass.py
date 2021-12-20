import logging
import multiprocessing
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class MyProcess(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logging.info('{} run() called'.format(self.name))
        time.sleep(2)
        logging.info('{} run() finished'.format(self.name))


def main():
    jobs = []
    for i in range(5):
        p = MyProcess(name='process-{}'.format(i))
        jobs.append(p)

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()


if __name__ == "__main__":
    main()
