from datetime import datetime, timedelta
import logging

import requests

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from db.influx import InfluxDatabase
from db.sqlite import SqliteDatabase


log = logging.getLogger('weather.backend.scheduler')

now = datetime.now()
next_run = now - timedelta(minutes=now.minute) - timedelta(hours=now.hour+6)

every_15_minutes = AndTrigger([
    DateTrigger(),
    IntervalTrigger(minutes=15, start_date=next_run)
])
every_12_hours = AndTrigger([
    DateTrigger(),
    IntervalTrigger(hours=12, start_date=next_run)
])
every_hour = AndTrigger([
    DateTrigger(),
    IntervalTrigger(hours=1, start_date=next_run)
])
scheduler = BackgroundScheduler()



def schedule_jobs(weather_data):
    for station in weather_data:
        # station_id = station["id"]
        # log.info(f'scheduling update tasks for {station_id}')

        log.info('scheduling forecast update')
        # scheduler.add_job(update_forecast, every_12_hours, args=[station, ])

        log.info('scheduling conditions update')
        scheduler.add_job(update_conditions, every_15_minutes, args=[station, ])

    log.info('scheduling space weather update')
    scheduler.add_job(update_space_weather, every_hour)

    log.info('scheduling alerts update')
    scheduler.add_job(update_alerts, every_hour)

# def update_forecast(station):
    # station_id = station["id"]
    # log.debug(f'opening connection to database for {station_id}')
    
    # with SqliteDatabase(station_id) as database:
    #     log.debug('downloading forecast data')
    #     r = requests.get(station["urls"]["forecast"])

    #     periods = r.json()["properties"]["periods"]

    #     log.debug(f'{periods}')
    #     database.submit_forecast(periods)

def update_conditions(station):
    log.debug('connection to current conditions database')
    with InfluxDatabase() as database:
        log.debug('downloading conditions data')
        r = requests.get(station["urls"]["conditions"])

        log.debug('adding to database')
        database.submit_conditions(station["id"], r.json())

def update_space_weather():
    log.debug('updated space weather but there was nothing to do...')

def update_alerts():
    log.debug('updated alerts but there was nothing to do...')
