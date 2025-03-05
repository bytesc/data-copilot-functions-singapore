import json
from typing import List, Tuple, Optional

import pandas as pd
from agent.utils.llm_access.LLM import get_llm

llm = get_llm()

from .map.get_onemap_minimap import get_minimap_func
from .map.utils.api_call import get_api_result_func


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
