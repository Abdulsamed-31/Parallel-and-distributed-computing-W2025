# from celery import Celery 

# app = Celery("tasks" , broker = "pyamqp://guest@localhost//")

# @app.task
# def power(num, power):
#     return num ** power

from celery import Celery

# Create a Celery instance
app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

@app.task
def power(x, y):
    return x ** y
