from datetime import datetime
import schedule


def schedule_task(f, interval=15, next_run=None):
    if next_run:
        schedule.every(interval).at(next_run).do(f)
    else:
        schedule.every(interval).minutes.do(f)
