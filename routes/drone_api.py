from dronekit import connect, VehicleMode
import os
from flask import Blueprint, Response, jsonify, request
from dotenv import load_dotenv

from drone.drone import getHud, getJSONState
from navigation.square_search import get_visibility_radius, square_search

load_dotenv(".env")

drone = Blueprint("drone", __name__, url_prefix="/drone")


def getIP():
    if bool(os.getenv("DEV")):
        return "tcp:127.0.0.1:5760"
    else:
        return os.getenv("DRONE_IP")


try:
    vehicle = connect(getIP(), heartbeat_timeout=0)
except:
    print("unable to connect to vehicle")


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


@drone.post("/api/search/square")
def square():
    if not request.is_json:
        return Response(status=400)
    content = request.json

    lat = content.get("lat")
    long = content.get("long")
    radius = content.get("radius")
    alt = content.get("alt")

    visibility_radius = get_visibility_radius(90, alt)

    path = square_search(lat, long, radius, visibility_radius)
    print(path)
    return jsonify(path)


@drone.post("/api/mode")
def set_mode():
    if not request.is_json:
        return Response(status=400)
    content = request.json

    mode = content.get("mode")
    try:
        vehicle.wait_for_mode(mode, timeout=10)
        res = {"success": True, "mode": vehicle.mode.name}
        return jsonify(res)
    except:
        res = {"success": False, "mode": vehicle.mode.name}
        return jsonify(res)


@drone.post("/api/takeoff")
def takeoff():
    if not vehicle.is_armable:
        return jsonify({"success": False})
    vehicle.wait_for_mode("GUIDED", timeout=10)
    vehicle.arm(wait=True)
    vehicle.wait_simple_takeoff(alt=50, timeout=30)
    return jsonify({"success": True})
