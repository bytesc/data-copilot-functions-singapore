import pandas as pd
import sqlalchemy
from typing import List, Tuple, Optional

from .utils.get_config import config_data
from .utils.llm_access.LLM import get_llm

DATABASE_URL = config_data['mysql']
engine = sqlalchemy.create_engine(DATABASE_URL)

STATIC_URL = config_data['static_path']

llm = get_llm()

from .copilot.sql_code import query_database_func
from .copilot.python_code import draw_graph_func
from .map.get_onemap_minimap import get_minimap_func


def query_database(question: str, df_cols: str | list = None) -> pd.DataFrame:
    """
    query_database(question: str, df_cols: str | list = None) -> pd.DataFrame:
    Query the database using natural language question. Can not query anything not included in the database content!!!
    Returns the query results in pandas DataFrame.

    Args:
    - question (str): Natural language question.
    - df_cols (str|list): The columns' names of the DataFrame(e.g. "uid, username, stu_num").

    Returns:
    - pd.DataFrame: A DataFrame containing the results of the database query.
        The DataFrame includes the columns provided in df_cols(the second args)

    Example:
    ```python
        ans_df = query_database('Select the grades of Jane Smith', df_cols='lesson_id, lesson_name, grade')
        # Output(pd.DataFrame):
        #        lesson_id lesson_name grade
        # 0        001  Mathematics     99.00
        # 1        002      English     88.50
        # 2        003     Physics    65.00
        # ... and so on(the structure of the output DataFrame id based on df_cols(the second input args))
    ```
    """

    result = query_database_func(question, df_cols, llm, engine)
    return result


def draw_graph(question: str, data: pd.DataFrame) -> str:
    """
    draw_graph(question: str, data: pd.DataFrame) -> str:
    Draw graph based on natural language graph type and data provided in a pandas DataFrame.
    Returns an url path string of the graph.

    Args:
    - question (str): Natural language graph type.
    - data (pd.DataFrame): A pandas DataFrame for providing drawing data.

    Returns:
    - str: url path string of the output graph.(e.g. "http://127.0.0.1:8003/tmp_imgs/mlkjcvep.png").

    Example:
    ```python
        data = pd.DataFrame({
            '月份': ['1月', '2月', '3月', '4月', '5月'],
            '销售额': [200, 220, 250, 210, 230]
        })
        graph_url = draw_graph("画折线图", data)
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/ekhidpcl.png"
    ```
    """
    result = draw_graph_func(question, data, llm)
    result = STATIC_URL + result[2:]
    return result


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

