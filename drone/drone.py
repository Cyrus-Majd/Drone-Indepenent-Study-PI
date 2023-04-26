# THIS WILL HAVE THE CURRENT DRONE STATE


def getJSONState(vehicle):
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
    return data


def getHud(vehicle):
    data = {
        "roll": vehicle.attitude.roll,
        "pitch": vehicle.attitude.pitch,
        "heading": vehicle.heading,
        "vario": vehicle.velocity[1],
        "airspeed": vehicle.airspeed,
        "altitude": vehicle.location.global_frame.alt,
    }
    return data


def getAtt(vehicle):
    return vehicle.location.global_frame.alt
