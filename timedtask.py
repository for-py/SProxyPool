from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from proxycheck import ProxyCheck
import random
import datetime
import time


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}


def task():
    pc = ProxyCheck()
    pc.check_valid()


# day_interval >= 1
def get_low_high(day_interval=3, start_hour=10, end_hour=22):
    start_timestamp = day_interval * 24 * 3600 + start_hour * 3600
    end_timestamp = day_interval * 24 * 3600 + end_hour * 3600

    current_time = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
    y, m, d = int(current_time[0]), int(current_time[1]), int(current_time[2])

    zero = datetime.datetime(y, m, d, 0, 0, 0)
    now = datetime.datetime.now()+datetime.timedelta(seconds=20)

    zero_timestamp = zero.timestamp()
    now_timestamp = now.timestamp()

    rand_low = start_timestamp - (now_timestamp - zero_timestamp)
    rand_high = end_timestamp - (now_timestamp - zero_timestamp)

    return int(rand_low), int(rand_high), now


low, high, day = get_low_high()
scheduler = BackgroundScheduler(executors=executors)

scheduler.add_job(task, trigger='date', run_date=day)
scheduler.start()

while True:
    time.sleep(random.randint(low, high))
    low, high, day = get_low_high()
    scheduler.add_job(task, trigger='date', run_date=day)
