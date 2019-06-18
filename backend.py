import json
import logging

from flask import Flask, render_template

from scheduler import schedule_jobs
from db.influx import InfluxDatabase
from db.sqlite import SqliteDatabase

log = logging.getLogger('weather.backend')
log.setLevel("DEBUG")


weather_data = {}
log.debug('reading and parsing weather data')
with open('weather_data.json', 'r') as fp:
    weather_data = json.load(fp)
    log.debug(f'{weather_data}')

schedule_jobs(weather_data)

app = Flask(__name__)

@app.route('/weather/<station_id>/conditions')
def conditions(station_id):
    conditions = None
    with InfluxDatabase() as database:
        conditions = database.current_conditions(station_id)
    
    context = { "conditions": conditions }
    return render_template('conditions.html', context=context)

@app.route('/weather/<station_id>/forecast')
def forecast(station_id):
    forecast = None
    with SqliteDatabase(station_id) as database:
        forecast = database.get_nday_forecast()
    
    context = { "forecast": forecast }
    return render_template('forecast.html', context=context)

