import logging
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS
from grow.moisture import Moisture

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# InfluxDB settings
TOKEN = "1CDjgTM9hqWsqclEAFJdFPE3SZj6yY3v21SK-OJcxRMxPcvQTzV0_zkgesn0fmhJJSvnikkRGEqWFVomyZUCoA=="
ORG = "enviro"
URL = "http://unraid.local:8086"
BUCKET = "grow-4"

# Initialize InfluxDB client and write API
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = WriteApi(influxdb_client=client, write_options=SYNCHRONOUS)

# Create moisture sensor instances
meters = [Moisture(i + 1) for i in range(3)]

# Main loop for reading and writing moisture and saturation values
while True:
    # Read moisture and saturation values and round to 3 decimal places
    moisture_values = [round(meter.moisture, 3) for meter in meters]
    saturation_values = [round(meter.saturation, 3) for meter in meters]

    # Write moisture values if they are non-zero
    if 0 in moisture_values:
        continue
    else:
        for i, moisture in enumerate(moisture_values, 1):
            point = Point(f"moisture-{i}").field("value", moisture)
            write_api.write(bucket=BUCKET, org=ORG, record=point)
            logging.info(f"Wrote {moisture} moisture-{i} to InfluxDB")

    # Write saturation values if they are not equal to 1.0
    if 1.0 in saturation_values:
        continue
    else:
        for i, saturation in enumerate(saturation_values, 1):
            point = Point(f"saturation-{i}").field("value", saturation)
            write_api.write(bucket=BUCKET, org=ORG, record=point)
            logging.info(f"Wrote {saturation} saturation-{i} to InfluxDB")
    # Wait for 60 seconds before reading and writing values again
    logging.info("Waiting 60 seconds before reading and writing values again")
    time.sleep(60)