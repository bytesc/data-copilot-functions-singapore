
import requests
from PIL import Image
from io import BytesIO

from .utils.get_onemap_auth import AUTH


def get_static_map(lat, lon, map_filename="map_image.png"):
    """
    Fetch a static map image from the OneMap API for the given latitude and longitude.

    Parameters:
        lat (float): Latitude of the map's center.
        lon (float): Longitude of the map's center.
        map_filename (str): Name of the file to save the map image. Default is 'map_image.png'.

    Returns:
        None: Saves the map as an image file.
    """
    # Base URL for the OneMap API
    url = f"https://www.onemap.gov.sg/api/staticmap/getStaticImage?layerchosen=default&latitude={lat}&longitude={lon}&zoom=17&width=400&height=512&points=[{lat},{lon}]"

    # Replace with your actual API token
    headers = {
        "Authorization": AUTH}

    # Make the request
    response = requests.get(url, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        # Load the image into PIL
        image = Image.open(BytesIO(response.content))

        # Save the image to the specified file
        image.save(map_filename)
        print(f"Map image saved as '{map_filename}'")
    else:
        print(f"Error: Unable to retrieve the image. Status code: {response.status_code}")
        print(response.text)


# Example usage
if __name__ == "__main__":
    get_static_map(1.31955, 103.84223, "static_map.png")