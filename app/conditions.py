import requests
from app.converters import c2f, kmh2mph, nothing


##
# update_conditions(url) - Update the current observations at a specific station
# @params: url - the address to query for updates
# @returns: conditions - dictionary containing the latest measurements for the specified station
##
def update(url):
    r = requests.get(url, headers={"Accept": "application/geo+json"})

    props: dict = r.json()['properties']
    
    conditions = {
        "icon": props["icon"].replace("medium", "large")
    }

    effects = ["temperature", "relativeHumidity", "windSpeed", "windDirection", "heatIndex", "dewpoint"]
    for fieldName in effects:
        if props[fieldName]["value"] is not None:
            conditions[fieldName] = __process_field(props[fieldName])
    
    return conditions


def __process_field(field: dict):
    conversions = {
        "unit:degC": c2f,
        "unit:km_h-1": kmh2mph,
        "unit:degree_(angle)": nothing,
        "unit:percent": nothing
    }

    conversion_func = conversions.get(field["unitCode"], nothing)
    return conversion_func(field["value"])
