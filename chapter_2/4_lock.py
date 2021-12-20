import threading

shared_resource_with_lock = 0
shared_resource_with_no_lock = 0
count = 100000
shared_resource_lock = threading.Lock()


def increment_with_lock():
    global shared_resource_with_lock
    for i in range(count):
        with shared_resource_lock:
            shared_resource_with_lock += 1


def decrement_with_lock():
    global shared_resource_with_lock
    for i in range(count):
        with shared_resource_lock:
            shared_resource_with_lock -= 1


def increment_without_lock():
    global shared_resource_with_no_lock
    for i in range(count):
        shared_resource_with_no_lock += 1


def decrement_without_lock():
    global shared_resource_with_no_lock
    for i in range(count):
        shared_resource_with_no_lock -= 1


def main():
    t1 = threading.Thread(target=increment_with_lock)
    t2 = threading.Thread(target=decrement_with_lock)
    t3 = threading.Thread(target=increment_without_lock)
    t4 = threading.Thread(target=decrement_without_lock)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print('Value with lock: {}'.format(shared_resource_with_lock))
    print('Value without lock: {}'.format(shared_resource_with_no_lock))


if __name__ == "__main__":
    main()
