import json
from typing import List, Tuple, Optional, Dict, Union

import pandas as pd
from agent.utils.llm_access.LLM import get_llm

from .tools_def import  engine
llm = get_llm()

from .map.get_onemap_minimap import get_minimap_func
from .map.utils.api_call import get_api_result_func
from .db.query_db import find_schools_near_postcode_func
from .map.map_cal import find_preschools_in_walking_distance_func


# def get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None,
#                 postcode_list: Optional[List[str]] = None) -> str:
#     """
#     get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None, postcode_list: Optional[List[str]] = None) -> str:
#     Generate an HTML iframe for a minimap with optional markers in latitude and longitude pairs or or postal codes.
#     Returns an HTML iframe string.
#
#     The function creates an HTML iframe that embeds a minimap from OneMap.sg.
#     Users can specify a list of latitude and longitude pairs or postal codes
#     to be marked on the map.
#
#     Args:
#     - lat_lng_list (Optional[List[Tuple[float, float]]]): A list of tuples,
#       where each tuple contains a latitude and longitude pair for a marker.
#       Default is None.
#     - postcode_list (Optional[List[str]]): A list of postal codes to be marked
#       on the map. Default is None.
#
#     Returns:
#     - str: An HTML iframe string that can be embedded in a webpage to display
#       the minimap with the specified markers.
#
#     Example usage:
#     ```python
#     get_minimap_func(lat_lng_list=[(1.2996492424497, 103.8447478575), (1.29963489170907, 103.845842317726)])
#     get_minimap_func(postcode_list=["123456"])
#     ```
#
#     """
#     html = get_minimap_func(lat_lng_list, postcode_list)
#     return html

def get_minimap(
        markers: Optional[List[Dict[str, Union[str, Tuple[float, float]]]]] = None
) -> str:
    """
    get_minimap(markers: Optional[List[Dict[str, Union[str, Tuple[float, float]]]]] = None) -> str:
    Generate an HTML iframe for a minimap with customizable markers and routes from OneMap.sg.
    Returns an HTML iframe string.

    The function creates an HTML iframe that embeds a minimap from OneMap.sg with
    customizable markers and optional routes between them. Destination points for
    routes must also be added as markers on the map!!!

    Args:
    - markers: List of marker dictionaries. Each marker can have:
        * 'location': Either a postalcode (str) or latLng tuple (float, float) (REQUIRED)
        * 'color': color from: 'red', 'blue', 'green', 'black' (REQUIRED)
        * 'icon': Optional icon name from: 'fa-user', 'fa-mortar-board', 'fa-subway', 'fa-bus', 'fa-star'
        * 'route_type': Optional route type from: 'TRANSIT', 'WALK', 'DRIVE'
        * 'route_dest': Optional destination for route as latLng tuple (float, float) Destination point must be added as another individual marker point in the list!!!

    Returns:
    - str: An HTML iframe string that can be embedded in a webpage to display
      the minimap with the specified markers and routes.

    Example usage(just example, do not use the data):
    ```python
    get_minimap([{'location': (1.29203, 103.843), 'color': 'red'}])
    dest = (1.33587, 103.854)
    get_minimap([{'location': "238889", 'color': 'black', 'icon': 'fa-bus', 'route_type': 'WALK', 'route_dest': dest}])
    ```

    """
    html = get_minimap_func(markers)
    return html


def get_api_result(url: str) -> dict | list:
    """
    get_api_result(url: str) -> dict | list:
    Get data from API (This API provides population data sets by the Department of Statistics. The types of population demographics data, based on planning area or subzone, include age group, economic status, education status, household size etc.) with Relative URL string
    Returns a JSON dict or list of the request result

    Args:
    - url (string): the Relative URL of the request, use Relative URL not Full URL !!!

    Returns:
    - dict | list: the JSON result of the request

    Example usage:
    ```python
    # use Relative URL not Full URL !!!
    get_api_result("/api/public/popapi/getEconomicStatus?planningArea=Bedok&year=2010&gender=male")
    ```
    """
    result = get_api_result_func(url)
    return result


from .prediction.Model_Deploy3 import predict_house_price
def house_price_prediction_model(month="", storey_range="", town="",
                                 flat_type="", flat_model="",
                                 street_name="", floor_area_sqm=1,
                                 lease_commence_date="", remaining_lease="") -> float:
    """
    house_price_prediction_model(month="", storey_range="", town="", flat_type="", flat_model="", street_name="", floor_area_sqm=1, lease_commence_date="", remaining_lease="") -> float:
    Predict the price of an HDB flat based on various property features.
    Returns the predicted price as a float value.

    The function uses a pre-trained machine learning model to estimate the price
    of an HDB flat given its characteristics. All parameters are optional with
    default values, but providing more accurate information will yield better predictions.

    Args:
    - month (str): Transaction month in "YYYY-MM" format. Default is empty string.
    - storey_range (str): Original floor range (e.g., "04 to 06"). Default is empty string.
    - town (str): Town where the flat is located. Default is empty string.
    - flat_type (str): Type of flat (e.g., "4-room"). Default is empty string.
    - flat_model (str): Model of flat (e.g., "Simplified"). Default is empty string.
    - street_name (str): Fine-grained location information. Default is empty string.
    - floor_area_sqm (float): Floor area in square meters. Default is 1.
    - lease_commence_date (str): Year lease commenced (e.g., "1985"). Default is empty string.
    - remaining_lease (str): Remaining lease duration (e.g., "59 years 11 months"). Default is empty string.

    Returns:
    - float: The predicted price of the HDB flat.

    Example usage:
    ```python
    price = house_price_prediction_model(
        month="2025-01",
        storey_range="04 to 06",
        town="YISHUN",
        flat_type="4-room",
        flat_model="Simplified",
        street_name="ANG MO KIO AVE 10",
        floor_area_sqm=84,
        lease_commence_date="1985",
        remaining_lease="59 years 11 months"
    )
    ```
    """
    sample_input = {
        "month": month,  # Transaction month
        "storey_range": storey_range,  # Original floor range
        "town": town,  # Town (provided here; if missing, will be replaced with "unknown")
        "flat_type": flat_type,
        "flat_model": flat_model,
        "street_name": street_name,  # Fine-grained location info
        "floor_area_sqm": floor_area_sqm,
        "lease_commence_date": lease_commence_date,
        "remaining_lease": remaining_lease
    }
    # sample_input = {
    #     "month": "2025-01",  # Transaction month
    #     "storey_range": "04 to 06",  # Original floor range
    #     "town": "YISHUN",  # Town (provided here; if missing, will be replaced with "unknown")
    #     "flat_type": "4-room",
    #     "flat_model": "Simplified",
    #     "street_name": "ANG MO KIO AVE 10",  # Fine-grained location info
    #     "floor_area_sqm": 84,
    #     "lease_commence_date": "1985",
    #     "remaining_lease": "59 years 11 months"
    # }
    pred, features_used, processed = predict_house_price(sample_input)
    return pred[0]


def find_schools_near_postcode(postcode: str, radius_km: float = 2.0) -> pd.DataFrame:
    """
    find_schools_near_postcode(postcode: str, radius_km: float = 2.0) -> pd.DataFrame:
    Find schools near a given postal code within a specified radius.
    Returns a pandas DataFrame containing school information.

    The function queries a database to find schools located within a certain distance
    (in kilometers) from the specified postal code. Each school's information includes
    name, address, contact details, and distance from the given postcode.

    Args:
    - postcode (str): The postal code to search around (e.g., "123456")
    - radius_km (float): Search radius in kilometers. Default is 2.0 km.

    Returns:
    - pd.DataFrame: A DataFrame where each row contains information about
      a school within the specified radius. Columns include:
        - school_name: Name of the school
        - address: Full address of the school
        - postcode: Postcode of the school
        - telephone: Contact telephone number
        - email: Email address
        - distance_km: Distance from the input postcode in kilometers

    Example usage:
    ```python
    schools_df = find_schools_near_postcode("139951", 1.5)

    # Output (pd.DataFrame):
    #                             school_name            address postcode telephone            email  distance_km
    # 0               NATIONAL JUNIOR COLLEGE  37 HILLCREST ROAD  288913  64667755  njc@moe.edu.sg          0.8
    # 1  ANGLO-CHINESE SCHOOL (INDEPENDENT)     121 DOVER ROAD   138650  67731611  acsind@acs.edu.sg         1.2
    #
    # [2 rows x 6 columns]
    ```
    """
    school_list = find_schools_near_postcode_func(postcode, engine, radius_km)
    return pd.DataFrame(school_list)


def find_preschools_in_walking_distance(postcode: str, walking_km: float = 2.0) -> pd.DataFrame:
    """
    find_preschools_in_walking_distance(postcode: str, walking_km: float = 2.0) -> pd.DataFrame:
    Find preschools within walking distance of a given postcode.
    Returns a pandas DataFrame containing preschool information with walking distance and time.

    The function first queries preschools within a straight-line distance from the specified postal code,
    then calculates actual walking routes to determine precise walking distances and times.
    Each preschool's information includes name, code, license details, and walking metrics.

    Args:
    - postcode (str): The postal code to search around (e.g., "123456")
    - walking_km (float): Initial straight-line search radius in kilometers. Default is 2.0 km.

    Returns:
    - pd.DataFrame: A DataFrame where each row contains information about
      a preschool within walking distance. Columns include:
        - centre_name: Name of the preschool
        - centre_code: Unique code of the preschool
        - latitude: Geographic latitude
        - longitude: Geographic longitude
        - walking_distance_km: Actual walking distance in kilometers
        - walking_time_min: Estimated walking time in minutes

    Example usage:
    ```python
    preschools_df = find_preschools_in_walking_distance("139951", 1.5)

    # Output (pd.DataFrame):
    #            centre_name centre_code  latitude  longitude class_of_licence  ...  fees type_of_citizenship walking_distance_km walking_time_min
    # 0  KIDZ MEADOW CHILDCARE     PC-0001    1.2345   103.4567         Full Day  ...  $800-$1200               All                 0.8             10.5
    #
    # [1 rows x 11 columns]
    ```
    """
    preschool_list = find_preschools_in_walking_distance_func(postcode, engine, walking_km)
    return pd.DataFrame(preschool_list)
