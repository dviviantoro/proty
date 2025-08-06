import os, sys
from influxdb_client_3 import InfluxDBClient3, Point
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

client = InfluxDBClient3(token=influx_token, host=influx_host, database=influx_database)

def influx_query(sql_sentence):
    result = client.query(query=sql_sentence, language="sql", mode="polars")
    return result

# print(influx_query("SELECT 'posMin' FROM 'pd-test' WHERE name = 'test acq' AND phase = '3'"))
# print(influx_query('SELECT "posMin" FROM "pd-test" WHERE name = \'test acq\' AND phase = \'0\''))
