import json, logging


log = logging.getLogger(__name__)

weather_data = {}
log.debug('reading and parsing weather data')
with open('/usr/src/app/weather_data.json', 'r') as fp:
    weather_data = json.load(fp)