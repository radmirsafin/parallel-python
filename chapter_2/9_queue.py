import logging
import threading
from queue import Queue
import time
import random

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class Producer(threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            logging.info('{}: item {} appended to queue'.format(self.name, item))
            time.sleep(1)


class Consumer(threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            logging.info('{}: item {} popped'.format(self.name, item))
            self.queue.task_done()


def main():
    queue = Queue()
    threads = list()
    threads.append(Producer(queue, name='Producer'))
    for i in range(4):
        threads.append(Consumer(queue, name='Consumer-{}'.format(i)))

    for th in threads:
        th.start()

    for th in threads:
        th.join()


if __name__ == "__main__":
    main()
