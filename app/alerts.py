import requests
from datetime import datetime, timedelta, timezone

monitored_regions = {
    "East Baton Rouge", "West Baton Rouge", "Livingston", "Ascension", "St. James", "St. Charles", "St. John the Baptist", "Fourchon", "Caddo", "Bossier", "Iberville"
}

def update(url):
    r = requests.get(url, headers={"Accept": "application/geo+json"})

    alerts = []
    raw_alerts = r.json()["features"]

    for alert in raw_alerts:
        expires = datetime.fromisoformat(alert["properties"]["expires"])
        if expires > datetime.now(timezone.utc):
            alerts.append({
                "headline": alert["properties"]["headline"],
                "expiration": expires.isoformat(),
                "severity": alert["properties"]["severity"],
                "affecting": __get_affected_region(alert["properties"]["areaDesc"])
            })
    
    return alerts


def __get_affected_region(areaDesc: str):
    # areaDesc comes in as semicolon-separated list of affected parishes/counties,
    # first we turn it into a set then intersect it with monitored_regions to get
    # the parishes we actually GASA. We then convert back to list so it will JSON

    areaSet = set(areaDesc.split('; '))

    return list(areaSet.intersection(monitored_regions))