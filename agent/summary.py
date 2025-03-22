from .tools.tools_def import engine, llm
from .tools.copilot.sql_code import get_db_info_prompt
from .tools.copilot.utils.call_llm_test import call_llm


def get_ans_summary_prompt(ans: str):
    pre_prompt = """
This is the assistant's answer.
Please summarize the assistant's answer.
    """

    ans_prompt = """
Here is assistant's answer:
""" + ans

    end_prompt = """ 
Remind:
1. The id and number from the database may be meaningless numbers or strings but they are already proven correct.
2. All the links and urls are already proven accessible.
3. All the functions imported and called in code are already proven right and reliable.
"""
    return pre_prompt + ans_prompt +  end_prompt


def get_ans_summary(ans: str):
    prompt = get_ans_summary_prompt(ans)
    ans = call_llm(prompt, llm)
    return ans.content
