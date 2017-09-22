#! /usr/bin/python3

# celery -A celery_test worker --loglevel=info
import time
from celery import Celery

# http://www.cnblogs.com/piperck/p/5391128.html
celery = Celery("celery_test",broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')

@celery.task
def sendmail(mail):
    print("m")
    time.sleep(2)
    print('mail end')
    return "is result"

