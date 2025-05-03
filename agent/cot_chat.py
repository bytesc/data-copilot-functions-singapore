
import logging


from .tools.tools_def import engine, llm


from .tools.copilot.sql_code import get_db_info_prompt


from .tools.get_function_info import get_function_info

from .tools.copilot.utils.call_llm_test import call_llm

from .tools.map.population_api import get_population_api_info
from .tools.custom_tools_def import get_api_result


def get_cot_chat_prompt(question):
    data_prompt = get_db_info_prompt(engine, simple=True)
    # rag_ans = rag_from_policy_func(question,llm,engine)
    rag_ans = ""
    # print(rag_ans)

    knowledge = "\nBase knowledge: \n" + rag_ans + "\n"
    database = "\nThe database content: \n" + data_prompt + "\n"

    function_set, function_info, function_import = get_function_info(question, llm)
    # print(function_info)
    if function_info == "solved":
        return "solved", rag_ans, []
    print(function_info)

    api_info = ""
    api_prompt = ""
    if get_api_result in function_set:
        api_info = get_population_api_info(question, llm)
        api_prompt = f""" 
        Here is the APIs you can call with the provided function:
        """
        print(api_info)

    pre_prompt = """ 
Please use the following functions to solve the problem.
If you think the problem can be solved in one step, please return a single word: "one" without any other thing or explanation.
Remind:
1. Please tell me how to solve the problem step by step with Natural language.
2. Do not mention code details.
3. The chain of thought should be simple, short and clear.
4. If you think it could not be solved, with what you have, ask the user to provide more information.
5. If there are multiple approaches to solve the problem, try all of them.
"""
    function_prompt = """ 
Here is the functions you can import and use:
"""
    example_ans = """
Example 1:
We can solve the problem step by step:
1. Step1
2. Step2
3. Step3

Example 2:
I need you to clarify .....

Example 3:
one
    """

    cot_prompt = "question:" + question + knowledge + database + pre_prompt + \
                 function_prompt + str(function_info) + \
                 api_prompt + str(api_info)+ example_ans
    return cot_prompt, rag_ans, function_import


def get_cot_chat(question: str):
    cot_prompt, rag_ans, function_import = get_cot_chat_prompt(question)
    ans = call_llm(cot_prompt, llm)
    return ans.content
