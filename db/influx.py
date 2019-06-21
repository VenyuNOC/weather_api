from datetime import datetime
import json
import logging

import influxdb


class InfluxDatabase:
    def __init__(self, host='localhost', port=8086, username='root', password='root', dbname='weather'):
        self.log = logging.getLogger('db.InfluxDatabase')

        self.__db_handle = influxdb.InfluxDBClient(host, port, username, password)
        self.log.debug(f'opened connection to database at http://{host}:{port}, u={username},p={password}')

        self.log.debug(f'creating database {dbname}')
        self.__db_handle.create_database(dbname)
        
        self.log.debug(f'switching to {dbname}')
        self.__db_handle.switch_database(dbname)
        
    def _reset_db(self):
        self.log.debug('requested db reset')
        to_drop = [item["name"] for item in self.__db_handle.get_list_database() if item["name"] != '_internal']

        for table in to_drop:
            self.log.debug(f'dropping and recreating {table}')
            self.__db_handle.drop_database(table)
            self.__db_handle.create_database(table)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_trace):
        self.__db_handle.close()
            
    def submit_conditions(self, station_id, json_data):
        properties = json_data["properties"]

        series_data = [
            {
                "measurement": "current_conditions",
                "tags": {
                    "station_id": station_id
                },
                "time": datetime.now(),
                "fields": {
                    "temperature": float(properties["temperature"]["value"]),
                    "dewpoint": float(properties["dewpoint"]["value"]),
                    "wind_speed": float(properties["windSpeed"]["value"]),
                    "wind_direction": properties["windDirection"]["value"],
                    "barometric_pressure": properties["barometricPressure"]["value"],
                    "relative_humidity": float(properties["relativeHumidity"]["value"]),
                    "heat_index": float(properties["heatIndex"]["value"])
                }
            }
        ]

        self.__db_handle.write_points(series_data)
    
    def current_conditions(self, station_id):
        query_string = f"""select *::field from current_conditions where "station_id" = '{station_id.upper()}' group by station_id order by time desc limit 1"""
        
        result = self.__db_handle.query(query_string, method="POST")

        data = next(result.get_points())

        self.log.debug(data)

        return data
        


if __name__ == "__main__":
    import requests

    logging.basicConfig(level="DEBUG")

    with InfluxDatabase(dbname='test') as database:
        r = requests.get("https://api.weather.gov/stations/KBTR/observations/latest")
        database.submit_conditions('BTR', r.json())

        conditions = database.current_conditions('BTR')
