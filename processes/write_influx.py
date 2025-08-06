import os, sys
from influxdb_client_3 import (
    InfluxDBClient3, InfluxDBError, Point, WritePrecision,
    WriteOptions, write_client_options)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

def parser_init():
    parser = argparse.ArgumentParser(description="Scope task")
    parser.add_argument(
        "-d",
        "--data",
        help="Scope task"
    )
    return parser

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

if __name__ == "__main__":
    args = parser_init().parse_args()
    dict_data = json.loads(args.data)
    print(f"writing to influx: {dict_data}")

    # log raw data
    # phase = dict_data["tags"]["phase"]
    # pathfile = temp_dir / f"sensor_phase_{phase}.csv"
    # raw_data = np.loadtxt(pathfile, delimiter=',')
    # dict_data["fields"]["raw"] = json.dumps(raw_data.tolist())

    client.write(Point.from_dict(dict_data), write_precision='s')