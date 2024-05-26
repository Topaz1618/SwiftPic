# celery_worker.py
from celery import Celery
from time import time,sleep

# 创建Celery应用
# broker 传递消息
# backend 存储内容
app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

# 定义任务
@app.task
def add(x, y):
    sleep(2)
    return x + y


# 启动Celery Worker
if __name__ == '__main__':
    app.worker_main(['worker', '--loglevel=info'])