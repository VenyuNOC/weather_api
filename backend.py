import json
import logging

from flask import Flask, render_template, request, jsonify, render_template
from flask.logging import default_handler
from scheduler import schedule_jobs

from config import config
from data import weather_data
from db.influx import InfluxDatabase
from db.sqlite import SqliteDatabase

from blueprints.weather import weather_app
from blueprints.weather_api import weather_api

app = Flask(__name__)
app.config.from_object(config)

log = app.logger

for logger in (
    logging.getLogger('db.InfluxDatabase'),
    logging.getLogger('db.SQLite'),
    logging.getLogger('weather.backend.scheduler')
):
    logger.addHandler(default_handler)
    logger.setLevel(logging.DEBUG)


schedule_jobs(weather_data)

app.register_blueprint(weather_app)
app.register_blueprint(weather_api)

@app.after_request
def allow_cross_origin(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


