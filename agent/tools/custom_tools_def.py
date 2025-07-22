import json
from typing import List, Tuple, Optional, Dict, Union

import pandas as pd
from matplotlib import pyplot as plt

from agent.utils.llm_access.LLM import get_llm
from .copilot.examples.path_tools import generate_img_path
from .llm_analysis.llm_predict_hdb import llm_predict_hdb_func, get_llm_predict_hdb_info

from .tools_def import engine, STATIC_URL

llm = get_llm()

from .map.get_onemap_minimap import get_minimap_func
from .map.utils.api_call import get_api_result_func
from .db.query_db import find_schools_near_postcode_func, get_hdb_info_by_postcode
from .map.map_cal import find_preschools_in_distance_func


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


def house_price_prediction_model(from_date: str, to_date: str, storey_range="", planarea="",
                                 flat_type="", flat_model="", street_name="",
                                 floor_area_sqm=84, lease_commence_date="",
                                 remaining_lease="") -> tuple[pd.DataFrame, str]:
    """
    def house_price_prediction_model(from_date: str, to_date: str, storey_range="", planarea="",flat_type="", flat_model="", street_name="", floor_area_sqm=84, lease_commence_date="", remaining_lease="") ->  tuple[pd.DataFrame, str]:
    Predict HDB flat prices for a date range based on various property features. The function is used to predict a specific hbd not hbd with features, it only works well if most of the parameters are provided!!!
    Returns a DataFrame with predicted prices for each month in the range, sorted by date and an image path of graph.

    Args:
    - from_date (str): Start date in "YYYY-MM" format.
    - to_date (str): End date in "YYYY-MM" format.
    - storey_range (str): Original floor range (e.g., "04 to 06"). Default is empty string.
    - planarea (str): Planarea where the flat is located. Default is empty string.
    - flat_type (str): Type of flat (e.g., "4-room"). Default is empty string.
    - flat_model (str): Model of flat (e.g., "Simplified"). Default is empty string.
    - street_name (str): Fine-grained location information. Default is empty string.
    - floor_area_sqm (float): Floor area in square meters. Default is 84.
    - lease_commence_date (str): Year lease commenced (e.g., "1985"). Default is empty string.
    - remaining_lease (str): Remaining lease duration (e.g., "59 years 11 months"). Default is empty string.

    Returns:
    - pd.DataFrame: A DataFrame with columns 'month' and 'predicted_price', sorted by month.
    - str: A string image path of line graph

    Example usage:
    ```python
    price_df, img_path = house_price_prediction_model_range(
        from_date="2025-01",
        to_date="2025-12",
        storey_range="04 to 06",
        planarea="YISHUN",
        flat_type="4-room",
        flat_model="Simplified",
        street_name="ANG MO KIO AVE 10",
        floor_area_sqm=84,
        lease_commence_date="1985",
        remaining_lease="59 years 11 months"
    )
    yield price_df
    # Output:
    #     month  predicted_price
    # 0  2025-01      450000.0
    # 1  2025-02      452000.0
    # 2  2025-03      455000.0
    #   ...     ...
    yield img_path
    ```
    """
    # Generate monthly date range
    date_range = pd.date_range(start=from_date, end=to_date, freq='MS').strftime("%Y-%m")
    predictions = []
    for month in date_range:
        sample_input = {
            "month": month,
            "storey_range": storey_range,
            "town": planarea,
            "flat_type": flat_type,
            "flat_model": flat_model,
            "street_name": street_name,
            "floor_area_sqm": floor_area_sqm,
            "lease_commence_date": lease_commence_date,
            "remaining_lease": remaining_lease
        }
        pred, features_used, processed = predict_house_price(sample_input)
        predictions.append({
            "month": month,
            "predicted_price": pred[0]
        })
    # Create DataFrame and sort by month
    result_df = pd.DataFrame(predictions)
    result_df = result_df.sort_values("month")

    path = generate_img_path()

    plt.figure(figsize=(10, 6))
    plt.plot(result_df['month'], result_df['predicted_price'], marker='o', linestyle='-', color='b')
    plt.title(f'HDB Price Prediction Trend\n{from_date} to {to_date}')
    plt.xlabel('Month')
    plt.ylabel('Predicted Price (SGD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()

    return result_df, STATIC_URL + path[2:]


def find_schools_near_postcode(postcode: str, radius_km: float = 2.0) -> pd.DataFrame:
    """
    find_schools_near_postcode(postcode: str, radius_km: float = 2.0) -> pd.DataFrame:
    Find schools near a given postal code within a specified radius.
    Returns a pandas DataFrame containing school information. return None if not found.

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
        - latitude: Geographic latitude
        - longitude: Geographic longitude
        - distance_km: Distance from the input postcode in kilometers

    Example usage:
    ```python
    schools_df = find_schools_near_postcode("139951", 1.5)
    yield schools_df
    # Output (pd.DataFrame):
    #                             school_name            address postcode telephone     email   latitude    longitude   distance_km
    # 0               NATIONAL JUNIOR COLLEGE  37 HILLCREST ROAD  288913  64667755  njc@moe.edu.sg  1.2345  103.4567   0.8
    # 1  ANGLO-CHINESE SCHOOL (INDEPENDENT)     121 DOVER ROAD   138650  67731611  acsind@acs.edu.sg    1.2345  103.4567    1.2
    #
    # [2 rows x 6 columns]
    ```
    """
    school_list = find_schools_near_postcode_func(postcode, engine, radius_km)
    return pd.DataFrame(school_list)


def find_preschools_near_postcode(postcode: str, radius_km: float = 2.0) -> pd.DataFrame:
    """
    find_preschools_near_postcode(postcode: str, radius_km: float = 2.0) -> pd.DataFrame:
    Find preschools within distance of a given postcode.
    Returns a pandas DataFrame containing preschool information with walking distance and time. return None if not found.

    The function first queries preschools within a straight-line distance from the specified postal code,
    then calculates actual walking routes to determine precise walking distances and times.
    Each preschool's information includes name, code, license details, and walking metrics.

    Args:
    - postcode (str): The postal code to search around (e.g., "123456")
    - radius_km (float): Search radius in kilometers. Default is 2.0 km.

    Returns:
    - pd.DataFrame: A DataFrame where each row contains information about
      a preschool within distance. Columns include:
        - centre_name: Name of the preschool
        - centre_code: Unique code of the preschool
        - latitude: Geographic latitude
        - longitude: Geographic longitude
        - walking_distance_km: Actual walking distance in kilometers
        - walking_time_min: Estimated walking time in minutes

    Example usage:
    ```python
    preschools_df = find_preschools_near_postcode("139951", 1.5)

    yield preschools_df
    # Output (pd.DataFrame):
    #            centre_name centre_code  latitude  longitude  walking_distance_km walking_time_min
    # 0  KIDZ MEADOW CHILDCARE     PC-0001    1.2345   103.4567        0.8             10.5
    #
    # [1 rows x 11 columns]
    ```
    """
    preschool_list = find_preschools_in_distance_func(postcode, engine, radius_km)
    return pd.DataFrame(preschool_list)


def get_hdb_info_with_postcode(postcode: str) -> dict:
    """
    get_hdb_info_with_postcode(postcode: str) -> dict:
    Retrieve HDB (Housing Development Board) information for a given postal code.
    Returns a dictionary containing comprehensive details about the HDB flat. return None if not found.

    The function first queries basic address information from the HDB database,
    then supplements it with the latest resale transaction data including
    flat characteristics and lease information. For leases, it calculates
    the remaining lease period based on standard 99-year HDB leases.

    If the user provide different information, follow the user's instruction and replace the returned result.

    Args:
    - postcode (str): The postal code to search for (e.g., "123456")

    Returns:
    - dict: A dictionary containing HDB information with the following keys:
        - planarea: Planning area of the HDB flat
        - flat_type: Type of flat (e.g., 3-room, 4-room)
        - flat_model: Model of the flat
        - street_name: Name of the street
        - floor_area_sqm: Floor area in square meters
        - lease_commence_date: Year when lease commenced
        - remaining_lease: String representing remaining lease duration
        - blk_no: Block number

        If no resale data is found, returns basic address information with
        a message indicating limited data availability.

    Example usage:
    ```python
    hdb_info = get_hdb_info_by_postcode("139951", engine)

    yield hdb_info
    # Output (dict):
    # {
    #     'planarea': 'BUKIT MERAH',
    #     'flat_type': '3 ROOM',
    #     'flat_model': 'New Generation',
    #     'street_name': 'REDHILL CLOSE',
    #     'floor_area_sqm': 67.0,
    #     'lease_commence_date': '1974',
    #     'remaining_lease': '50 years 6 months',
    #     'blk_no': '89',
    # }
    ```
    """
    # example 750404
    hdb_info = get_hdb_info_by_postcode(postcode, engine)
    return hdb_info


def predict_hdb_price(from_date: str = None, to_date: str = None, plan_area=None, blk_no=None, street=None,
                      flat_model=None, flat_type=None, storey_range=None,
                      floor_area_sqm_from=None, floor_area_sqm_to=None,
                      lease_commence_date_from=None, lease_commence_date_to=None) -> tuple[pd.DataFrame, str]:
    """
def predict_hdb_price(from_date: str, to_date: str, plan_area=None, blk_no=None, street=None,flat_model=None, flat_type=None, storey_range=None,floor_area_sqm_from=None, floor_area_sqm_to=None,lease_commence_date_from=None, lease_commence_date_to=None) -> tuple[pd.DataFrame, str]:
Predict HDB resale prices for a date range based on various property features. The function is used to predict a kind of hdb with certain features, it works well even only some of the parameters provided!!!
The function returns both predicted prices dataFrame and a path of image of historical vs predicted prices.

Args:
- from_date (str, optional): Start date for prediction in "YYYY-MM" format.
- to_date (str, optional): End date for prediction in "YYYY-MM" format.
- plan_area (str, optional): Planning area where the flat is located (e.g., "ANG MO KIO").
- blk_no (str, optional): Block number of the HDB flat.
- street (str, optional): Street name where the flat is located (e.g., "ANG MO KIO AVENUE 1").
- flat_model (str, optional): Model of flat (e.g., "IMPROVED", "NEW GENERATION").
- flat_type (str, optional): Type of flat (e.g., "1 ROOM", "3 ROOM").
- storey_range (str, optional): Storey range (e.g., "04 TO 06", "10 TO 12").
- floor_area_sqm_from (float, optional): Minimum floor area in square meters for filtering.
- floor_area_sqm_to (float, optional): Maximum floor area in square meters for filtering.
- lease_commence_date_from (int, optional): Minimum lease commence year for filtering.
- lease_commence_date_to (int, optional): Maximum lease commence year for filtering.

Returns:
- pd.DataFrame: A DataFrame containing predicted prices with columns:
    * 'month': Prediction month in "YYYY-MM" format
    * 'predicted_price': Predicted resale price in SGD
- str: File path to the generated visualization image showing historical and predicted prices

Example usage:
```python
price_df, img_path = predict_hdb_price(
    from_date="2025-01",
    to_date="2025-12",
    plan_area="ANG MO KIO",
    flat_type="3 ROOM",
    flat_model="NEW GENERATION",
    street="ANG MO KIO AVENUE 1",
    storey_range="04 TO 06",
    floor_area_sqm_from=65,
    floor_area_sqm_to=75,
    lease_commence_date_from=1975,
    lease_commence_date_to=1980
)
yield price_df
    # Output:
    #     month  predicted_price
    # 0  2025-01      450000.0
    # 1  2025-02      452000.0
    # 2  2025-03      455000.0
    #   ...     ...
yield img_path
```
    """
    predict_df = llm_predict_hdb_func(engine=engine, llm=llm, from_date=from_date, to_date=to_date,
                                      plan_area=plan_area, blk_no=blk_no, street=street,
                                      flat_model=flat_model, flat_type=flat_type, storey_range=storey_range,
                                      floor_area_sqm_from=floor_area_sqm_from, floor_area_sqm_to=floor_area_sqm_to,
                                      lease_commence_date_from=lease_commence_date_from,
                                      lease_commence_date_to=lease_commence_date_to)
    search_conditions, hdb_price_history, sample = get_llm_predict_hdb_info(engine,
                                                                            plan_area=plan_area, blk_no=blk_no,
                                                                            street=street,
                                                                            flat_model=flat_model, flat_type=flat_type,
                                                                            storey_range=storey_range,
                                                                            floor_area_sqm_from=floor_area_sqm_from,
                                                                            floor_area_sqm_to=floor_area_sqm_to,
                                                                            lease_commence_date_from=lease_commence_date_from,
                                                                            lease_commence_date_to=lease_commence_date_to)
    path = generate_img_path()

    import matplotlib.pyplot as plt
    import pandas as pd
    from matplotlib.dates import AutoDateLocator, ConciseDateFormatter

    # Convert to datetime for proper plotting
    history_df = pd.DataFrame(hdb_price_history)
    history_df['month'] = pd.to_datetime(history_df['month'])
    predict_df['month'] = pd.to_datetime(predict_df['month'])

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # Plot historical data as scatter points
    if 'avg_resale_price' in history_df.columns:
        plt.scatter(history_df['month'], history_df['avg_resale_price'],
                    label='Historical Data Points', color='blue', alpha=0.6)
        y_values = history_df['avg_resale_price']
    elif 'resale_price' in history_df.columns:
        plt.scatter(history_df['month'], history_df['resale_price'],
                    label='Historical Data Points', color='blue', alpha=0.6)
        y_values = history_df['resale_price']

    # Create smoothed curve (using moving average)
    if len(history_df) > 1:
        # Sort by date first
        history_df = history_df.sort_values('month')
        # Calculate rolling average with window size based on data length
        window_size = max(2, min(6, len(history_df) // 3))
        smooth_df = history_df.copy()
        if 'avg_resale_price' in smooth_df.columns:
            smooth_df['smoothed'] = smooth_df['avg_resale_price'].rolling(window=window_size, center=True).mean()
        else:
            smooth_df['smoothed'] = smooth_df['resale_price'].rolling(window=window_size, center=True).mean()

        # Interpolate any NaN values at the ends
        smooth_df['smoothed'] = smooth_df['smoothed'].interpolate()

        # Plot the historical trend line
        plt.plot(smooth_df['month'], smooth_df['smoothed'],
                 label='Historical Trend', color='green', linewidth=2)

        # Get the last historical point for connection
        last_historical_date = smooth_df['month'].iloc[-1]
        last_historical_price = smooth_df['smoothed'].iloc[-1]

        # Get the first predicted point
        first_predicted_date = predict_df['month'].iloc[0]
        first_predicted_price = predict_df['predicted_price'].iloc[0]

        # Plot connecting line between historical and predicted
        plt.plot([last_historical_date, first_predicted_date],
                 [last_historical_price, first_predicted_price],
                 color='green', linestyle='--', alpha=0.5)

    # Plot predicted prices
    plt.plot(predict_df['month'], predict_df['predicted_price'],
             label='Predicted Price', linestyle='-', color='red')

    # Smart date formatting
    locator = AutoDateLocator()
    formatter = ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.xlabel('Date')
    plt.ylabel('Price (SGD)')
    plt.title('HDB Resale Price History and Prediction')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    # # Convert to datetime for proper plotting
    # history_df = pd.DataFrame(hdb_price_history)
    # history_df['month'] = pd.to_datetime(history_df['month'])
    # predict_df['month'] = pd.to_datetime(predict_df['month'])
    #
    # plt.figure(figsize=(12, 6))
    # ax = plt.gca()
    #
    # if 'avg_resale_price' in history_df.columns:
    #     plt.plot(history_df['month'], history_df['avg_resale_price'],
    #              label='Historical Average Price', marker='o', color='blue')
    # elif 'resale_price' in history_df.columns:
    #     plt.plot(history_df['month'], history_df['resale_price'],
    #              label='Historical Price', marker='o', color='blue')
    #
    # plt.plot(predict_df['month'], predict_df['predicted_price'],
    #          label='Predicted Price', linestyle='--', marker='x', color='red')
    #
    # # Smart date formatting
    # locator = AutoDateLocator()
    # formatter = ConciseDateFormatter(locator)
    # ax.xaxis.set_major_locator(locator)
    # ax.xaxis.set_major_formatter(formatter)
    #
    # plt.xlabel('Date')
    # plt.ylabel('Price (SGD)')
    # plt.title('HDB Resale Price History and Prediction')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.savefig(path)
    # plt.close()

    return predict_df, STATIC_URL + path[2:]
