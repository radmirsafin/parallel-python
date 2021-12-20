import logging
import threading
import time

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class MyThread(threading.Thread):
    def __init__(self, counter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.counter = counter

    def run(self):
        logging.info('{} started'.format(self.name))

        while not self._stop_event.is_set():
            if self.counter:
                logging.info('{} work'.format(self.name))
                time.sleep(5)
                self.counter -= 1
            else:
                self.stop()

        logging.info('{} exiting'.format(self.name))

    def stop(self):
        self._stop_event.set()


def main():
    thread1 = MyThread(1, name='FirstThread')
    thread2 = MyThread(2, name='SecondThread')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    logging.info('{} exiting'.format(threading.current_thread().getName()))


if __name__ == "__main__":
    main()
