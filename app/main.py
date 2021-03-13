import json

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import conditions, alerts


###########
# GLOBALS #
###########
latest_conditions = {
    "btr": {},
    "shv": {}
}
latest_alerts = []
weather_data = {}



### ###
#     #
# API #
#     #
### ###
def conditions_route(request):
    station = request.path_params["station"]
    return JSONResponse(latest_conditions.get(station, {}))

def alerts_route(request):
    return JSONResponse(latest_alerts)

def startup():
    global latest_alerts
    global latest_conditions
    global weather_data
    
    with open("weather_data.json", "r") as fp:
        weather_data = json.load(fp)
    
    latest_alerts = alerts.update(weather_data["alerts"])
    for key in latest_conditions.keys():
        latest_conditions[key] = conditions.update(weather_data["conditions"][key])
    
routes = [
    Route('/api/v1/conditions/{station}', conditions_route),
    Route('/api/v1/alerts', alerts_route)
]

app = Starlette(debug=True, routes=routes, on_startup=[startup,])

###       ###
#           #
# SCHEDULER #
#           #
###       ###
scheduler = BackgroundScheduler()
every_five_minutes = IntervalTrigger(0, 0, 0, 5)
every_hour = IntervalTrigger(0, 0, 1)

@scheduler.scheduled_job(every_five_minutes)
def update_shv_conditions():
    global weather_data
    global latest_conditions

    latest_conditions = conditions.update(weather_data["conditions"]["shv"])

@scheduler.scheduled_job(every_five_minutes)
def update_btr_conditions():
    global weather_data
    global latest_conditions

    latest_conditions = conditions.update(weather_data["conditions"]["btr"])

@scheduler.scheduled_job(every_hour)
def update_alerts():
    global weather_data
    global latest_alerts

    latest_alerts = alerts.update(weather_data["alerts"])