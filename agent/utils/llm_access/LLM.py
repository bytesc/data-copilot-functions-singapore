

from .get_api import get_api_key_from_file

from openai import OpenAI
from utils.get_config import config_data

def get_llm():
    llm = OpenAI(api_key=get_api_key_from_file("./agent/utils/llm_access/api_key_openai.txt"),
                 base_url=config_data["model_url"])
    # https://dashscope.aliyuncs.com/compatible-mode/v1
    # https: // api.deepseek.com / v1
    return llm
