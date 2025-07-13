import os, sys
from influxdb_client_3 import InfluxDBClient3, Point
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

client = InfluxDBClient3(token=influx_token, host=influx_host, database=influx_database)

def influx_write(data):
    dict_structure = {  
        "measurement": "pd",
        "tags": {
            "name": data["name"],
            "location": data["location"],
            "phase": None,
        }
    }

    points = []
    for i in range(0,3):
        dict_structure["tags"]["phase"] = i
        dict_structure["fields"] = {"water_level": float(i)}
        points.append(Point.from_dict(dict_structure))

    client.write(points, write_precision='s')

def influx_query(sql_sentence):
    result = client.query(query=sql_sentence, language="sql", mode="polars")
    return result

# data = {
#     "name": "saya",
#     "location": "marison"
# }

# influx_write(data)
# print(query("select * from home"))
# print(query("select * from pd"))
