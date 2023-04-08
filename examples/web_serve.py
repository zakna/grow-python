from functools import partial
import json
import logging
from aiohttp import web
from grow.moisture import Moisture

# Customize the JSON response function
json_response = partial(web.json_response, dumps=partial(json.dumps, default=str))

# Define the route table for the web server
routes = web.RouteTableDef()


# Define the /moisture endpoint to get moisture data
@routes.get("/moisture")
async def get_moisture(request):
    moisture_data = {
        "moisture-1": meter[0].moisture,
        "moisture-2": meter[1].moisture,
        "moisture-3": meter[2].moisture,
    }
    return json_response(moisture_data)


# Define the /saturation endpoint to get saturation data
@routes.get("/saturation")
async def get_saturation(request):
    saturation_data = {
        "m1": meter[0].saturation,
        "m2": meter[1].saturation,
        "m3": meter[2].saturation,
    }
    return json_response(saturation_data)


# Define the /range endpoint to get range data
@routes.get("/range")
async def get_range(request):
    range_data = {
        "m1": meter[0].range,
        "m2": meter[1].range,
        "m3": meter[2].range,
    }
    return json_response(range_data)

@routes.get("/data")
async def get_data(request):
    data = {
        "range": meter[0].range,
        "moisture": meter[0].moisture,
        "saturation": meter[0].saturation,
        "history": meter[0].history,
        "active": meter[0].active,
        "new_data": meter[0].new_data
    }
    return json_response(data)
# Main execution starts here
if __name__ == "__main__":
    # Create a web application instance
    app = web.Application()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Add routes to the web application
    app.add_routes(routes)

    # Initialize moisture sensors
    meter = [Moisture(_ + 1) for _ in range(3)]

    # Run the web application on host 0.0.0.0 and port 8080 with custom log format
    web.run_app(
        app,
        host="0.0.0.0",
        port=8080,
        access_log_format='%s %r [%b / %Tf] "%{User-Agent}i"',
    )
