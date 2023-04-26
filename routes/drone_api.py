from dronekit import connect
import os
from flask import Blueprint, Response, jsonify, request
from dotenv import load_dotenv

from drone.drone import getHud, getJSONState

load_dotenv(".env")

drone = Blueprint("drone", __name__, url_prefix="/drone")


def getIP():
    if os.getenv("DEV"):
        return "tcp:127.0.0.1:5760"
    else:
        return os.getenv("DRONE_IP")


vehicle = connect(getIP(), heartbeat_timeout=0)


@drone.route("/api/hud")
def hud():
    data = getHud(vehicle)
    return jsonify(data)


@drone.route("/api/json")
def json():
    data = getJSONState(vehicle)
    return jsonify(data)


@drone.post("/api/arm")
def arm():
    if vehicle.armed:
        vehicle.disarm()
    else:
        vehicle.arm()
    return jsonify(
        {
            "drone_arm": vehicle.armed,
        }
    )


@drone.post("/api/search_area")
def search():
    if not request.is_json:
        return Response(status=400)
    content = request.json

    lat = content.lat
    long = content.long
    radius = content.radius
    att = vehicle.location.global_frame.alt
