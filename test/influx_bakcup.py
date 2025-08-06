import os, sys
# from influxdb_client_3 import InfluxDBClient3, Point
from influxdb_client_3 import (
    InfluxDBClient3, InfluxDBError, Point, WritePrecision,
    WriteOptions, write_client_options)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

def success(self, data: str):
    print(f"Successfully wrote batch: data: {data}")

def error(self, data: str, exception: InfluxDBError):
    print(f"Failed writing batch: config: {self}, data: {data} due: {exception}")

def retry(self, data: str, exception: InfluxDBError):
    print(f"Failed retry writing batch: config: {self}, data: {data} retry: {exception}")

# Configure options for batch writing.
write_options = WriteOptions(batch_size=500,
                                    flush_interval=10_000,
                                    jitter_interval=2_000,
                                    retry_interval=5_000,
                                    max_retries=5,
                                    max_retry_delay=30_000,
                                    exponential_base=2)

# Create an options dict that sets callbacks and WriteOptions.
wco = write_client_options(success_callback=success,
                          error_callback=error,
                          retry_callback=retry,
                          write_options=write_options)


client = InfluxDBClient3(token=influx_token, host=influx_host, database=influx_database, write_client_options=wco)

def influx_write(dict_data):
    client.write(Point.from_dict(dict_data), write_precision='s')

# def influx_write(data):
#     dict_structure = {  
#         "measurement": "pd",
#         "tags": {
#             "name": data["name"],
#             "location": data["location"],
#             "phase": None,
#         }
#     }

#     points = []
#     for i in range(0,3):
#         dict_structure["tags"]["phase"] = i
#         dict_structure["fields"] = {"water_level": float(i)}


#         points.append(Point.from_dict(dict_structure))

#     client.write(points, write_precision='s')

def influx_query(sql_sentence):
    result = client.query(query=sql_sentence, language="sql", mode="polars")
    return result

# data = {
#     "name": "saya",
#     "location": "marison"
# }

# influx_write(data)
# print(query("select * from home"))
# print(influx_query("select * from pd"))

# for i in range(10):
# print(influx_query("SELECT 'posMin' FROM 'pd-test' WHERE name = 'test acq' AND phase = '3'"))
print(influx_query('SELECT "posMin" FROM "pd-test" WHERE name = \'test acq\' AND phase = \'0\''))
