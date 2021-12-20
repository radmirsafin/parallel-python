import asyncio
import time
from random import randint


@asyncio.coroutine
def start_state():
    print("S0 called")
    input_value = randint(0, 1)
    time.sleep(1)
    if input_value == 0:
        result = yield from state_2(input_value)
    else:
        result = yield from state_1(input_value)
    print("Resume of the Transition: \n" + result)


@asyncio.coroutine
def state_1(transition_value):
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = yield from state_3(input_value)
    else:
        result = yield from state_2(input_value)
    return "state 1 calling with value {}\n{}".format(transition_value, result)


@asyncio.coroutine
def state_2(transition_value):
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = yield from state_1(input_value)
    else:
        result = yield from state_3(input_value)
    return "state 2 calling with value {}\n{}".format(transition_value, result)


@asyncio.coroutine
def state_3(transition_value):
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = yield from state_1(input_value)
    else:
        result = yield from end_state(input_value)
    return "state 3 calling with value {}\n{}".format(transition_value, result)


@asyncio.coroutine
def end_state(transition_value):
    print("...stop computation...")
    return "end_state calling with value {}\n".format(transition_value)


if __name__ == '__main__':
    print("Finite State Machine simulation with Asyncio Coroutine")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_state())
