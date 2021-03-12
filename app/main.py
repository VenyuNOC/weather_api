import json

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from app import conditions, alerts


latest_conditions = {
    "btr": {},
    "shv": {}
}
latest_alerts = []

def conditions(request):
    pass

def alerts(request):
    pass

def startup():
    with open("weather_data.json", "r") as fp:
        weather_data = json.load(fp)

    latest_alerts = alerts.update(weather_data["alerts"])
    for key in latest_conditions.keys():
        latest_conditions[key] = conditions.update(weather_data["conditions"][key])
    
    