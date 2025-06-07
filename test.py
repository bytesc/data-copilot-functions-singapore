from agent.tools.map.population_api import get_api_select_prompt
# get_api_select_prompt("q")
# from agent.tools.custom_tools_def import get_api_result
# get_api_result("/api/public/popapi/getEconomicStatus?planningArea=Bedok&year=2020")

import sqlalchemy

from agent.utils.get_config import config_data
from agent.utils.llm_access.LLM import get_llm

DATABASE_URL = config_data['mysql']
engine = sqlalchemy.create_engine(DATABASE_URL)

STATIC_URL = config_data['static_path']

llm = get_llm()
