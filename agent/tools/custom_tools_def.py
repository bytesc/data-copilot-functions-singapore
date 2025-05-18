import json
from typing import List, Tuple, Optional

import pandas as pd
from agent.utils.llm_access.LLM import get_llm

from .tools_def import  engine
llm = get_llm()

from .map.get_onemap_minimap import get_minimap_func
from .map.utils.api_call import get_api_result_func
from .prediction.Model_Deploy3 import predict_house_price
from .db.query_db import find_schools_near_postcode_func


def get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None,
                postcode_list: Optional[List[str]] = None) -> str:
    """
    get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None, postcode_list: Optional[List[str]] = None) -> str:
    Generate an HTML iframe for a minimap with optional markers in latitude and longitude pairs or or postal codes.
    Returns an HTML iframe string.

    The function creates an HTML iframe that embeds a minimap from OneMap.sg.
    Users can specify a list of latitude and longitude pairs or postal codes
    to be marked on the map.

    Args:
    - lat_lng_list (Optional[List[Tuple[float, float]]]): A list of tuples,
      where each tuple contains a latitude and longitude pair for a marker.
      Default is None.
    - postcode_list (Optional[List[str]]): A list of postal codes to be marked
      on the map. Default is None.

    Returns:
    - str: An HTML iframe string that can be embedded in a webpage to display
      the minimap with the specified markers.

    Example usage:
    ```python
    get_minimap_func(lat_lng_list=[(1.2996492424497, 103.8447478575), (1.29963489170907, 103.845842317726)])
    get_minimap_func(postcode_list=["123456"])
    ```

    """
    html = get_minimap_func(lat_lng_list, postcode_list)
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


def find_schools_near_postcode(postcode: str, radius_km: float = 2.0) -> list:
    """
    find_schools_near_postcode(postcode: str, radius_km: float = 2.0) -> list:
    Find schools near a given postal code within a specified radius.
    Returns a list of dictionaries containing school information.

    The function queries a database to find schools located within a certain distance
    (in kilometers) from the specified postal code. Each school's information includes
    name, address, contact details, and distance from the given postcode.

    Args:
    - postcode (str): The postal code to search around (e.g., "123456")
    - radius_km (float): Search radius in kilometers. Default is 2.0 km.

    Returns:
    - list: A list of dicts where each dictionary contains information about
      a school within the specified radius. Each dictionary includes:
        - school_name: Name of the school
        - address: Full address of the school
        - postal_code: Postal code of the school
        - telephone: Contact telephone number
        - email: Email address
        - mrt: Nearby MRT stations
        - bus: Nearby bus services
        - latitude: Geographic latitude
        - longitude: Geographic longitude
        - distance_km: Distance from the input postcode in kilometers

    Example usage:
    ```python
    schools = find_schools_near_postcode("139951", 1.5)

    # Output(list):
    # [
    #     {
    #         "school_name": "NATIONAL JUNIOR COLLEGE",
    #         "address": "37 HILLCREST ROAD",
    #         "postal_code": "288913",
    #         "telephone": "64667755",
    #         "email": "njc@moe.edu.sg",
    #         "mrt": "Newton (NS21,DT11)",
    #         "bus": "48, 66, 67, 170, 171, 700, 960",
    #         "latitude": 1.3156,
    #         "longitude": 103.844,
    #         "distance_km": 0.8
    #     },
    #     {
    #         "school_name": "ST. MARGARET'S SECONDARY SCHOOL",
    #         "address": "111 FARRER ROAD",
    #         "postal_code": "259240",
    #         "telephone": "64745666",
    #         "email": "stmargarets@moe.edu.sg",
    #         "mrt": "Farrer Road (CC20)",
    #         "bus": "48, 93, 153, 165, 174, 852",
    #         "latitude": 1.3123,
    #         "longitude": 103.842,
    #         "distance_km": 1.2
    #     },
    #     ...
    # ]
    ```
    """
    school_list = find_schools_near_postcode_func(postcode, engine, radius_km)
    return school_list
