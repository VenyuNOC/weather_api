import os

from flask import request, jsonify
from flask import Blueprint, render_template, abort


from db.influx import InfluxDatabase
from db.sqlite import SqliteDatabase

from data import weather_data


weather_app = Blueprint("weather", __name__, template_folder=os.path.join('templates', 'weather'))


@weather_app.route('/weather/<station_id>/conditions')
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

    return render_template('conditions.html', **context)

@weather_app.route('/weather/<station_id>/forecast')
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

    return render_template('forecast.html', **context)

@weather_app.route('/weather/tropical')
def tropical():
    atlantic = weather_data["global"]["urls"]["tropical"]["atlantic"]
    pacific = weather_data["global"]["urls"]["tropical"]["pacific"]

    context = {
        'atlantic': atlantic,
        'pacific': pacific
    }

    if 'kiosk' in request.args.keys():
        context['next'] = ''.join((request.url_root, '/'.join(('weather', 'btr', 'conditions'))))

    return render_template('tropical.html', **context)

def get_long_name(station_id):
    for station in weather_data["locations"]:
        if station["id"] == station_id.upper():
            return station["display_name"]
        
    return "Unknown"
