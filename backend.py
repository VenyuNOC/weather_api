import json
import logging

from flask import Flask, render_template, request, jsonify
from flask.logging import default_handler

from scheduler import schedule_jobs
from db.influx import InfluxDatabase
from db.sqlite import SqliteDatabase

app = Flask(__name__)

log = app.logger

for logger in (
    logging.getLogger('db.InfluxDatabase'),
    logging.getLogger('db.SQLite'),
    logging.getLogger('weather.backend.scheduler')
):
    logger.addHandler(default_handler)
    logger.setLevel(logging.DEBUG)

weather_data = {}
log.debug('reading and parsing weather data')
with open('weather_data.json', 'r') as fp:
    weather_data = json.load(fp)

schedule_jobs(weather_data)

@app.route('/weather/<station_id>/conditions')
def conditions(station_id):
    conditions = None
    with InfluxDatabase() as database:
        conditions = database.current_conditions(station_id)
    
    context = {
        'conditions': conditions,
        'station_id': station_id,
        'long_name': get_long_name(station_id)
    }
    
    if 'kiosk' in request.args.keys():
        if station_id.lower() == 'btr':
            context['next'] = ''.join((request.url_root, '/'.join(('weather', 'shv', 'conditions'))))
        else:
            context['next'] = ''.join((request.url_root, '/'.join(('weather', 'btr', 'forecast'))))

    return jsonify(context)

@app.route('/weather/<station_id>/forecast')
def forecast(station_id):
    forecast = None
    with SqliteDatabase(station_id) as database:
        forecast = database.get_nday_forecast()
        
    context = {
        'forecast': forecast["periods"],
        'station_id': station_id,
        'long_name': get_long_name(station_id)
    }

    if 'kiosk' in request.args.keys():
        if station_id.lower() == 'btr':
            context['next'] = ''.join((request.url_root, '/'.join(('weather', 'shv', 'forecast'))))
        else:
            context['next'] = ''.join((request.url_root, '/'.join(('weather', 'tropical'))))

    return jsonify(context)

@app.route('/weather/tropical')
def tropical():
    atlantic = weather_data["global"]["urls"]["tropical"]["atlantic"]
    pacific = weather_data["global"]["urls"]["tropical"]["pacific"]

    context = {
        'atlantic': atlantic,
        'pacific': pacific
    }

    if 'kiosk' in request.args.keys():
        context['next'] = ''.join((request.url_root, '/'.join(('weather', 'btr', 'conditions'))))

    return jsonify(context)

def get_long_name(station_id):
    for station in weather_data["locations"]:
        if station["id"] == station_id.upper():
            return station["display_name"]
        
    return "Unknown"
