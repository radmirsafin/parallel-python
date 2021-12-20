import logging
import multiprocessing
import random
import time


LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class Producer(multiprocessing.Process):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            logging.info('Producer add item: {}'.format(item))
            time.sleep(1)
            logging.info('Queue size: {}'.format(self.queue.qsize()))


class Consumer(multiprocessing.Process):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break

            time.sleep(2)
            item = self.queue.get()
            logging.info('Consumer pop item: {}'.format(item))
            time.sleep(1)


def main():
    queue = multiprocessing.Queue()

    producer = Producer(queue, name='Producer')
    consumer = Consumer(queue, name='Consumer')

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()


if __name__ == "__main__":
    main()
