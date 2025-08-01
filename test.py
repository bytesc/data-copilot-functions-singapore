from agent.tools.custom_tools_def import predict_hdb_price
from agent.tools.map.population_api import get_api_select_prompt
# get_api_select_prompt("q")
# from agent.tools.custom_tools_def import get_api_result
# get_api_result("/api/public/popapi/getEconomicStatus?planningArea=Bedok&year=2020")

# from agent.tools.custom_tools_def import find_preschools_in_walking_distance, find_schools_near_postcode
# find_schools_near_postcode("380101", 3.0)
# find_preschools_in_walking_distance("380101", 2.0)

# import sqlalchemy
#
# from agent.utils.get_config import config_data
# from agent.utils.llm_access.LLM import get_llm
#
# DATABASE_URL = config_data['mysql']
# engine = sqlalchemy.create_engine(DATABASE_URL)
#
# STATIC_URL = config_data['static_path']
#
# llm = get_llm()
df,path = predict_hdb_price(from_date="2025-04", to_date="2028-01", plan_area="CLEMENTI", flat_type="3 ROOM",
                            lease_commence_date_from=2000, lease_commence_date_to=2025)
print(df,path)