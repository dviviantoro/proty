import os, sys
import pandas as pd
from influxdb_client_3 import InfluxDBClient3, Point
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

client = InfluxDBClient3(token=influx_token, host=influx_host, database=influx_database)

def influx_query(sql_sentence):
    result = client.query(query=sql_sentence, language="sql", mode="pandas")
    
    # result["time"] = pd.to_datetime(result['time'])
    result["time"] = result["time"].astype(str)
    # print(result["time"].dtypes)
    # print(result["time"])

    base_columns = ['time', 'location', 'name', 'phase']
    measure_columns = [col for col in result.columns if col not in base_columns]
    numpy_arrays = {}

    for measure_col in measure_columns:
        numpy_arrays[measure_col] = result[['time', measure_col]].to_numpy().tolist()

    return numpy_arrays

# print(influx_query("SELECT 'posMin' FROM 'pd-test' WHERE name = 'test acq' AND phase = '3'"))
# print(influx_query('SELECT "posMin" FROM "pd-test" WHERE name = \'test acq\' AND phase = \'0\''))
# print(type(influx_query('SELECT * FROM "pd-test" WHERE name = \'test acq\' AND phase = \'1\'')))

# result = influx_query('SELECT * FROM "pd-test" WHERE name = \'test acq\' AND phase = \'1\'')
# print(result["negCnt"])