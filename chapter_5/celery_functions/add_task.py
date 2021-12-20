from celery import Celery

app = Celery('tasks', broker='pyamqp://root:123@192.168.122.138//')


@app.task
def add(x, y):
    return x + y
