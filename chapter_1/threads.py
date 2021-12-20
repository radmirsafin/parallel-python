import logging
import threading
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class CookBook(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = "Hello Parallel Python CookBook!!"

    def print_message(self):
        print('Thread print message: {}'.format(self.message))

    def start(self):
        logging.info('{} thread started'.format(self.name))
        super().start()

    def run(self):
        x = 0
        while x < 5:
            self.print_message()
            time.sleep(0.5)
            x += 1
        logging.info("Thread {} ended".format(self.name))


def main():
    logging.info('Main process started')

    threads = []
    for i in range(5):
        threads.append(CookBook(name='CookBookThread-{}'.format(i)))

    for thread in threads:
        thread.start()

    logging.info('Main process ended')


if __name__ == "__main__":
    main()
