import threading


def func(thread_number):
    print('function called by thread {}'.format(thread_number))


def main():
    threads = []
    for i in range(5):
        t = threading.Thread(target=func, args=(i,))
        threads.append(t)
        t.start()
        t.join()


if __name__ == "__main__":
    main()
