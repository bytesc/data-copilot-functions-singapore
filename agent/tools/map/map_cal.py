from geopy.distance import geodesic
from typing import Optional, Tuple


def calculate_distance_km(coord1: Tuple[float, float],
                          coord2: Tuple[float, float]) -> Optional[float]:
    """
    Calculate the geodesic distance between two coordinates in kilometers.

    Args:
        coord1: Tuple of (latitude, longitude) in decimal degrees
        coord2: Tuple of (latitude, longitude) in decimal degrees

    Returns:
        Distance in kilometers as float if successful, None if invalid input

    Examples:
        >>> calculate_distance_km((40.7128, -74.0060), (34.0522, -118.2437))
        3935.328919218516
    """
    try:
        # Validate coordinate ranges
        for coord in (coord1, coord2):
            lat, lon = coord
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError(f"Invalid coordinate range: {coord}")

        # Calculate and return distance in km
        distance = geodesic(coord1, coord2).kilometers
        return float(distance)  # Explicit conversion to float

    except (ValueError, TypeError) as e:
        print(f"[Error] Invalid coordinates: {e}")
        return 0.0
    except Exception as e:
        print(f"[Error] Distance calculation failed: {e}")
        return 0.0


from agent.tools.db.query_db import find_preschools_near_postcode_func, postcode_to_location
from agent.tools.map.utils.api_call import get_api_result_func


def find_preschools_in_distance_func(postcode: str, engine, radius_km: float = 2.0):
    # Get preschools within initial straight-line distance
    pre_schools = find_preschools_near_postcode_func(postcode, engine, radius_km)
    latitude, longitude = postcode_to_location(postcode, engine)

    if not latitude or not longitude:
        raise ValueError(f"Could not find location for postcode {postcode}")

    start_point = f"{latitude},{longitude}"
    result = []

    for preschool in pre_schools:
        end_point = f"{preschool['latitude']},{preschool['longitude']}"

        try:
            # Get walking route information
            route_data = get_api_result_func(
                f"/api/public/routingsvc/route?start={start_point}&end={end_point}&routeType=walk"
            )

            if route_data.get("status") == 0:  # Successful route
                route_summary = route_data.get("route_summary", {})
                total_distance = route_summary.get("total_distance", 0)  # in meters
                total_time = route_summary.get("total_time", 0)  # in seconds

                # Create result dictionary with all original fields
                preschool_result = {
                    'centre_name': preschool['centre_name'],
                    'centre_code': preschool['centre_code'],
                    'latitude': preschool['latitude'],
                    'longitude': preschool['longitude'],
                    'walking_distance_km': round(total_distance / 1000, 2),  # Convert to km with 2 decimal places
                    'walking_time_min': round(total_time / 60, 1)  # Convert to minutes with 1 decimal place
                }
                # if (total_distance / 1000) <= radius_km:
                #     result.append(preschool_result)
                result.append(preschool_result)

        except Exception as e:
            print(f"Error getting route for preschool {preschool['centre_code']}: {e}")
            continue

    # Sort by walking distance
    result.sort(key=lambda x: x['walking_distance_km'])

    return result
