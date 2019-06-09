from datetime import datetime
import influxdb


class InfluxDatabase:
    class Datapoint:
        def __init__(self, measurement, station_id, value):
            self.measurement = measurement
            self.station_id = station_id
            self.value = value
        
        def to_json(self):
            return f"""[
    {{
        "measurement": {self.measurement},
        "tags": {{
            "station_id": {self.station_id}
        }},
        "time": {datetime.now()},
        "fields": {{
            "value": {self.value}
        }}
    }}
]"""
    
    def __init__(self, host='localhost', port=8086, username='root', password='root', dbname=None):
        self.__db_handle = influxdb.InfluxDBClient(host, port, username, password)

        if dbname is not None and dbname not in self.__db_handle.get_list_database():
            self.__db_handle.create_database(dbname)
        
    def __enter__(self):
        return self

    def __exit(self, exc_type, exc_value, traceback):
        self.__db_handle.close()

    def write_point(self, station_id, measurement, value):
        self.__db_handle.write(Datapoint(measurement, station_id, value).to_json())
