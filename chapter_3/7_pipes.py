import logging
import multiprocessing


LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def create_items(items_client_tip):

    for item in range(5000):
        items_client_tip.send(item)
        logging.info('Item created: {}'.format(item))

    items_client_tip.close()


def multiply_items(items_server_tip, result_client_tip):

    try:
        while True:
            item = items_server_tip.recv()
            result = item * item
            logging.info('Item received {} and processed {}'.format(item, result))
            result_client_tip.send(result)
    except EOFError:
        items_server_tip.close()
        result_client_tip.close()


def main():
    items_server_tip, items_client_tip = multiprocessing.Pipe()

    process_pipe_1 = multiprocessing.Process(target=create_items, args=(items_client_tip,))
    process_pipe_1.start()
    items_client_tip.close()

    result_server_tip, result_client_tip = multiprocessing.Pipe()

    process_pipe_2 = multiprocessing.Process(target=multiply_items, args=(items_server_tip, result_client_tip))
    process_pipe_2.start()
    items_server_tip.close()

    result_client_tip.close()

    result = 0
    try:
        while True:
            result += result_server_tip.recv()
    except EOFError:
        result_server_tip.close()

    logging.info('RESULT: {}'.format(result))


if __name__ == "__main__":
    main()
