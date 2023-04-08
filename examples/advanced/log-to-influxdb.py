import logging
import time

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS

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
bucket = "grow"

# Create a synchronous write API instance
write_api = WriteApi(influxdb_client=write_client, write_options=SYNCHRONOUS)

# Loop through 5 iterations to create and write 5 data points
for value in range(10):

    # Create a data point using the Point class with the moisture measurement
    point = (
        Point("moisture")

        # Add a tag to the data point
        .tag("tagname1", "tagvalue1")

        # Add a field to the data point with its value set to the current iteration
        .field("value", value)
    )

    # Write the data point to the InfluxDB
    write_api.write(bucket=bucket, org="enviro", record=point)

    # Sleep for 1 second to separate each data point by a 1-second interval
    time.sleep(2)

    # Log the data point that was written to InfluxDB
    logging.info(f"  - wrote {value} to InfluxDB")
