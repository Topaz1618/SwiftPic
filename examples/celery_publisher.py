# celery publisher

from celery import Celery
from time import time,sleep

# 创建Celery应用
app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

# 发布任务
task1 = app.send_task('tasks.add', args=[4, 6])

task2 = app.send_task('tasks.add', args=[2, 4])

while True:
    res = task1.get()
    if res:
        print("Task1 res:", res)
        break
    sleep(1)


print("Task2 res:", task2.get())  # 获取任务结果