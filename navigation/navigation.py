import math


def move_point(lat, lon, bearing, distance):
    # Earth's radius in meters
    R = 6378137

    # Convert lat/lon to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing)

    # Calculate new latitude and longitude
    new_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(distance / R)
        + math.cos(lat_rad) * math.sin(distance / R) * math.cos(bearing_rad)
    )
    new_lon_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(distance / R) * math.cos(lat_rad),
        math.cos(distance / R) - math.sin(lat_rad) * math.sin(new_lat_rad),
    )

    # Convert new lat/lon back to degrees
    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)

    return new_lat, new_lon


def square_search(center_lat, center_long, max_radius, visibility_radius):
    pattern = [(center_lat, center_long)]
    visibility_diameter = 2* visibility_radius
    visibility_multiplier = 1
    max_range_in_terms_of_VR = max_radius / visibility_diameter
    current_lat = center_lat
    current_long = center_long

    while max_range_in_terms_of_VR > visibility_multiplier / 2:
        current_lat, current_long = move_point(
            current_lat, current_long, 0, visibility_multiplier * visibility_diameter
        )
        pattern.append((current_lat, current_long))

        current_lat, current_long = move_point(
            current_lat, current_long, 270, visibility_multiplier * visibility_diameter
        )
        pattern.append((current_lat, current_long))

        visibility_multiplier += 1

        current_lat, current_long = move_point(
            current_lat, current_long, 180, visibility_multiplier * visibility_diameter
        )
        pattern.append((current_lat, current_long))

        current_lat, current_long = move_point(
            current_lat, current_long, 90, visibility_multiplier * visibility_diameter
        )
        pattern.append((current_lat, current_long))

        visibility_multiplier += 1

    return pattern

def linear_search(center_lat, center_long, max_radius, visibility_radius):

    start_lat, start_long = move_point(center_lat,center_long,225,max_radius * math.sqrt(2))
    max_diameter = max_radius*2
    pattern = [(start_lat,start_long)]
    search_length = 0
    current_lat = start_lat
    current_long = start_long
    while search_length < max_diameter:
        current_lat, current_long = move_point(
            current_lat, current_long, 180*((search_length/visibility_radius) % 2), max_diameter
        )
       

        pattern.append((current_lat, current_long))
        current_lat, current_long = move_point(
            current_lat, current_long, 90, visibility_radius
        )
        pattern.append((current_lat, current_long))
        search_length += visibility_radius

        #extra check
        if search_length >= max_diameter:
            break
        

    return pattern

"""
takes the camera FOV angle (in degrees) and the drone's current altitude (in meters) and returns the visiblity radius of
the camera(in meters).

"""
def get_visibility_radius(camera_angle, altitude):
    theta = math.radians(camera_angle/2)
    return altitude * math.tan(theta)