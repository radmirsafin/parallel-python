import add_task

if __name__ == '__main__':
    result = add_task.add.delay(4, 4)
    print(result)
