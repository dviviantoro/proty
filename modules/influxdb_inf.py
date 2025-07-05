import os
from influxdb_client_3 import (
    InfluxDBClient3, InfluxDBError, Point, WritePrecision,
    WriteOptions, write_client_options)

host = "http://localhost:8181"
token = "apiv3_S-Aq3ykD2D1FR8msCnyAIskLTCqcVIA550MR51R70axcYZX-kRSYYFszng9oKGpyMr7vJ459itg6lK9aY4IHig"
database = "test"

def success(self, data: str):
    print(f"Successfully wrote batch: data: {data}")

def error(self, data: str, exception: InfluxDBError):
    print(f"Failed writing batch: config: {self}, data: {data} due: {exception}")

def retry(self, data: str, exception: InfluxDBError):
    print(f"Failed retry writing batch: config: {self}, data: {data} retry: {exception}")

write_options = WriteOptions(batch_size=500,
                                    flush_interval=10_000,
                                    jitter_interval=2_000,
                                    retry_interval=5_000,
                                    max_retries=5,
                                    max_retry_delay=30_000,
                                    exponential_base=2)

wco = write_client_options(success_callback=success,
                          error_callback=error,
                          retry_callback=retry,
                          write_options=write_options)

def influx_write(data):
    # client = InfluxDBClient3(token=token, host=host, database=database, write_client_options=wco)
    points = [Point("home")
            .tag("room", "Kitchen")
            .field("temp", 25.1)
            .field('hum', 20.2)
            .field('co', 9)]
    # # print(points)
    # client.write(points, write_precision='s')
    with InfluxDBClient3(host=host,
                        token=token,
                        database=database,
                        write_client_options=wco) as client:

        client.write(points, write_precision='s')

def query():
    client = InfluxDBClient3(token=token, host=host, database=database)
    query = "select * from home"
    reader = client.query(query=query, language="sql", mode="polars")
    print(reader)
    return reader

influx_write("33")
# query()