import asyncio


# sum of n integers
async def first_coroutine(future, N):
    count = 0
    for i in range(1, N + 1):
        count = count + i
    await asyncio.sleep(4)
    future.set_result("First coroutine: {}".format(count))


# factorial
async def second_coroutine(future, N):
    count = 1
    for i in range(2, N + 1):
        count *= i
    await asyncio.sleep(3)
    future.set_result("Second coroutine: {}".format(count))


def got_result(future):
    print(future.result())


if __name__ == '__main__':
    N1 = 1
    N2 = 2

    loop = asyncio.get_event_loop()
    future1 = asyncio.Future()
    future2 = asyncio.Future()

    tasks = [
        first_coroutine(future1, N1),
        second_coroutine(future2, N2),
    ]

    future1.add_done_callback(got_result)
    future2.add_done_callback(got_result)

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
