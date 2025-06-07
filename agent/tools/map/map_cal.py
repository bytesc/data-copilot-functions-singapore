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
