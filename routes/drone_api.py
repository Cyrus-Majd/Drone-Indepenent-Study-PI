from dronekit import connect
import os
from flask import Blueprint, jsonify
from dotenv import load_dotenv

load_dotenv(".env")

drone = Blueprint("drone", __name__, url_prefix="/drone")


def getIP():
    if os.getenv("DEV"):
        return "tcp:127.0.0.1:5760"
    else:
        return os.getenv("DRONE_IP")


vehicle = connect(getIP(), heartbeat_timeout=0)


@drone.route("/api/json")
def json():
    gps = {
        "lat": vehicle.location.global_frame.lat,
        "long": vehicle.location.global_frame.lon,
        "att": vehicle.location.global_frame.alt,
    }
    data = {
        "info": {
            "drone_name": "THE DRONE",
            "drone_gps": gps,
            "drone_battery": vehicle.battery.level,
            "drone_heart": "{:10.2f}s".format(vehicle.last_heartbeat),
            "drone_armable": vehicle.is_armable,
            "drone_status": vehicle.system_status.state,
            "drone_mode": vehicle.mode.name,
        },
        "direction": {
            "drone_head": vehicle.heading,
            "drone_att": gps.get("att"),
            "drone_vel": vehicle.velocity,
            "drone_air_speed": vehicle.airspeed,
            "drone_ground_speed": vehicle.groundspeed,
            "drone_arm": vehicle.armed,
            "drone_home": vehicle.home_location,
        },
    }
    return jsonify(data)
