import json
import logging
import signal

from scheduler import scheduler, schedule_jobs

from data import weather_data
from db.influx import InfluxDatabase


default_handler = logging.StreamHandler()

for logger in (
    logging.getLogger('db.InfluxDatabase'),
    logging.getLogger('weather.backend.scheduler')
):
    logger.addHandler(default_handler)
    logger.setLevel(logging.DEBUG)

def shutdown(signalNumber, frame):
    global interrupted
    interrupted = True

    if scheduler.running:
        scheduler.shutdown(wait=False)


signal.signal(signal.SIGTERM, shutdown)
interrupted = False


if __name__ == "__main__":
    while not interrupted:
        if not scheduler.running:
            schedule_jobs(weather_data)
