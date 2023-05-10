from dronekit import connect, VehicleMode, LocationGlobal
import os,threading,time
from flask import Blueprint, Response, jsonify, request
from dotenv import load_dotenv
from drone.drone import getHud, getJSONState
from navigation.navigation import get_visibility_radius, square_search, linear_search

load_dotenv(".env")

drone = Blueprint("drone", __name__, url_prefix="/drone")
drone_location = []
doingPath = False
vehicle = None

def getIP():
    if bool(os.getenv("DEV")):
        return "tcp:127.0.0.1:5760"
    else:
        return os.getenv("DRONE_IP")
    
def check_vehicle():
    if vehicle is None:
        try:
            print("trying to connect to ", getIP())
            vehicle = connect(getIP(), wait_ready=True, baud=57600)
            print("Connnected to drone!!")
        except:
            print("unable to connect to vehicle")

def check_thread():
    while True:
        check_vehicle
        time.wait(10)


try:
    print("trying to connect to ", getIP())
    vehicle = connect(getIP(), wait_ready=True, baud=57600)
    print("Connnected to drone!!")
except:
    print("unable to connect to vehicle")

check = threading.Thread(target=check_thread)
check.start()

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
    return jsonify(path)

@drone.post("/api/search/linear")
def linear():
    if not request.is_json:
        return Response(status=400)
    content = request.json

    lat = content.get("lat")
    long = content.get("long")
    radius = content.get("radius")
    alt = content.get("alt")

    visibility_radius = get_visibility_radius(90, alt)

    path = linear_search(lat, long, radius, visibility_radius)
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
    target_alt = 25
    if not vehicle.is_armable:
        return jsonify({"success": False})
    vehicle.wait_for_mode("GUIDED", timeout=10)
    vehicle.arm(wait=True)
    vehicle.wait_simple_takeoff(alt=target_alt, timeout=30)
    vehicle.wait_for_alt(alt=target_alt)
    return jsonify({"success": True})


@drone.post("/api/execute_path")
def execute_path():
    if not request.is_json:
        return Response(status=400)
    content = request.json
    global doingPath
    if doingPath:
        return jsonify({"success": False, "error": "already in path"})

    path = content.get("path").get("g")
    alt = content.get("alt")
    doingPath = True
    for target in path:
        if vehicle.mode.name == "RTL" or vehicle.mode.name == "SMARTRTL":
            doingPath = False
            return jsonify({"success": False})
        poll_location()
        current_loc = LocationGlobal(target.get("lat"), target.get("lng"), alt)
        vehicle.simple_goto(location=current_loc)
    doingPath = False
    return jsonify({"success": True})


def poll_location():
    drone_location.append(
        {
            "lat": vehicle.location.global_frame.lat,
            "long": vehicle.location.global_frame.lon,
            "att": vehicle.location.global_frame.alt,
        }
    )


@drone.post("/api/my_path")
def my_path():
    return jsonify(drone_location)


@drone.post("/api/land")
def land():
    vehicle.mode = VehicleMode("LAND")
    return jsonify({"status": "landed"})

@drone.post("/api/twirl")
def twirl():
    vehicle.condition_yaw(360,relative = True)
    return jsonify({"status": "twirling"})