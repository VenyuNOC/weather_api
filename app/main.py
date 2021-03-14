from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from scheduler import scheduler, get_latest_conditions, get_latest_alerts


def conditions_route(request):
    station = request.path_params["station"]
    return JSONResponse(get_latest_conditions(station))

def alerts_route(request):
    return JSONResponse(get_latest_alerts())

def startup():
    scheduler.start()

def shutdown():
    scheduler.stop(wait=False)

routes = [
    Route('/api/v1/conditions/{station}', conditions_route),
    Route('/api/v1/alerts', alerts_route)
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]

app = Starlette(debug=True, routes=routes, middleware=middleware, on_startup=[startup,], on_shutdown=[shutdown, ])
