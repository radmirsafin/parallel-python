import multiprocessing


def function_square(data):
    result = data*data
    return result


def main():
    data = list(range(100))

    pool = multiprocessing.Pool(processes=5)
    pool_outputs = pool.map(function_square, data)

    pool.close()
    pool.join()

    print('Pool results: {}'.format(pool_outputs))


if __name__ == "__main__":
    main()
