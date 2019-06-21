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

schedule_jobs(weather_data)

app = Flask(__name__)

@app.route('/weather/<station_id>/conditions')
def conditions(station_id):
    conditions = None
    with InfluxDatabase() as database:
        conditions = database.current_conditions(station_id)
    
    return render_template('conditions.html', conditions=conditions, station_id=station_id, long_name=get_long_name(station_id))

@app.route('/weather/<station_id>/forecast')
def forecast(station_id):
    forecast = None
    with SqliteDatabase(station_id) as database:
        forecast = database.get_nday_forecast()
    
    print(forecast)
    return render_template('forecast.html', forecast=forecast["periods"], station_id=station_id, long_name=get_long_name(station_id))

def get_long_name(station_id):
    for station in weather_data["locations"]:
        if station["id"] == station_id.upper():
            return station["display_name"]
        
    return "Unknown"
