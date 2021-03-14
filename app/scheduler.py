import json
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import conditions, alerts

latest_conditions = {
    "btr": {},
    "shv": {}
}
latest_alerts = []

scheduler = BackgroundScheduler()
every_five_minutes = IntervalTrigger(0, 0, 0, 5)
every_hour = IntervalTrigger(0, 0, 1)

with open("weather_data.json", "r") as fp:
    global weather_data
    weather_data = json.load(fp)
    print(weather_data)

@scheduler.scheduled_job(every_five_minutes, next_run_time=datetime.now())
def update_shv_conditions():
    global weather_data
    global latest_conditions

    print("downloading latest condition data for SHV")
    latest_conditions["shv"] = conditions.update(weather_data["conditions"]["shv"])
    print(latest_conditions["shv"])

@scheduler.scheduled_job(every_five_minutes, next_run_time=datetime.now())
def update_btr_conditions():
    global weather_data
    global latest_conditions

    print("downloading latest condition data for BTR")
    latest_conditions["btr"] = conditions.update(weather_data["conditions"]["btr"])
    print(latest_conditions["btr"])

@scheduler.scheduled_job(every_hour, next_run_time=datetime.now())
def update_alerts():
    global weather_data
    global latest_alerts

    print("downloading latest weather alert data")
    latest_alerts = alerts.update(weather_data["alerts"])
    print(latest_alerts)


def get_latest_conditions(station):
    global latest_conditions
    return latest_conditions.get(station)

def get_latest_alerts():
    global latest_alerts
    return latest_alerts