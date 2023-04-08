import logging
import time

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS
from grow.moisture import Moisture


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up InfluxDB
INFLUXDB_TOKEN = "1CDjgTM9hqWsqclEAFJdFPE3SZj6yY3v21SK-OJcxRMxPcvQTzV0_zkgesn0fmhJJSvnikkRGEqWFVomyZUCoA=="
token = INFLUXDB_TOKEN
org = "enviro"
url = "http://unraid.local:8086"

# Create an InfluxDB client instance
write_client = InfluxDBClient(url=url, token=token, org=org)

# Name of the bucket to write data to
bucket = "grow-4"

# Create a synchronous write API instance
write_api = WriteApi(influxdb_client=write_client, write_options=SYNCHRONOUS)

# Initialize moisture sensors
meter = [Moisture(_ + 1) for _ in range(3)]

# the moisture value is zero until the first reading is taken
moisture1 = meter[0].moisture
moisture2 = meter[0].moisture
moisture3 = meter[0].moisture
time.sleep(5)
moisture1 = meter[0].moisture
moisture2 = meter[0].moisture
moisture3 = meter[0].moisture

# Main execution starts here
while True:
    moisture1 = meter[0].moisture
    moisture2 = meter[1].moisture
    moisture3 = meter[2].moisture
    logging.info(f"Writing data point {moisture1} to InfluxDB...")
    # Create a data point using the Point class with the moisture measurement
    point1 = (
        Point("moisture-1")
        # Add a field to the data point with its value set to the current iteration
        .field("value", moisture1)
    )

    point2 = (
        Point("moisture-2").field("value", moisture2)
    )

    point3 = (
        Point("moisture-3").field("value", moisture3)
    )

    # Write the data point to the InfluxDB
    write_api.write(bucket=bucket, org="enviro", record=point1)
    logging.info(f"  - wrote {moisture1} to InfluxDB")
    write_api.write(bucket=bucket, org="enviro", record=point2)
    logging.info(f"  - wrote {moisture2} to InfluxDB")
    write_api.write(bucket=bucket, org="enviro", record=point3)
    logging.info(f"  - wrote {moisture3} to InfluxDB")
    # Sleep for 1 second to separate each data point by a 1-second interval
    time.sleep(5)

    # Log the data point that was written to InfluxDB
