

from .get_api import get_api_key_from_file

from openai import OpenAI


def get_llm():
    llm = OpenAI(api_key=get_api_key_from_file("./agent/tools/utils/llm_access/api_key_openai.txt"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    return llm
