import threading
import timeit


def function_to_run():
    pass


class SimpleSolver:
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()


class ThreadedSolver(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func

    def run(self):
        self.func()


def solve_without_thread(iterations):
    funcs = []
    for i in range(iterations):
        funcs.append(SimpleSolver(function_to_run))
    for i in funcs:
        i.run()


def solve_with_thread(iterations):
    funcs = []
    for i in range(iterations):
        funcs.append(ThreadedSolver(function_to_run))
    for i in funcs:
        i.run()


def test():
    repeat = 2
    number = 1
    threads_count = [1, 2, 4, 8]

    for i in threads_count:
        t = timeit.Timer('solve_without_thread({})'.format(i), "from __main__ import solve_without_thread")
        best_result = min(t.repeat(repeat, number))
        print('With {} iterations: \t{:4.6f} seconds'.format(i, best_result))

        t = timeit.Timer('solve_with_thread({})'.format(i), "from __main__ import solve_with_thread")
        best_result = min(t.repeat(repeat, number))
        print('With {} thread: \t\t{:4.6f} seconds'.format(i, best_result))


def main():
    global function_to_run

    print('********** Test 1 **********')
    test()

    print('********** Test 2 **********')

    def test2():
        a, b = 0, 1
        for a in range(10000):
            a, b = a, a + b

    function_to_run = test2
    test()

    print('********** Test 3 **********')

    def test3():
        size = 1024
        with open('test', 'rb') as file:
            for i in range(1000):
                file.read(size)
    function_to_run = test3
    test()

    print('********** Test 4 **********')

    def test4():
        import urllib.request
        for i in range(2):
            with urllib.request.urlopen('https://www.yandex.ru/') as page:
                page.read(1024)

    function_to_run = test4
    test()


if __name__ == "__main__":
    main()
