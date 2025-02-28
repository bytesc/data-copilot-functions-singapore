from .tools.tools_def import engine, llm
from .tools.copilot.sql_code import get_db_info_prompt
from .tools.copilot.utils.call_llm_test import call_llm


def get_ans_review_prompt(question: str, ans: str, code: str):
    question_prompt = """
Here is the user's question:
""" + question

    code_prompt = """
Here is code assistant's used to generate the answer, 
all the functions imported and called in it are already proven right and reliable:
""" + "```python\n" + code + "\n```\n" + '''
If any example input or default value for user to replace with actual data, problem not solved!!!
'''

    ans_prompt = """
Here is assistant's code's result:
""" + ans

    data_prompt = "The database content we have: \n" +\
                  get_db_info_prompt(engine, simple=True, example=True) + "\n"

    end_prompt = """ 
This is the user's question and the assistant's answer.
Is the problem solved?
If it is solved, summarize the assistant's answer.
If it is not, tell the reason and ask the user to provide further information.


Remind:
1. The id and number from the database may be meaningless numbers or strings but they are already proven correct.
2. All the links and urls are already proven accessible.
3. All the functions imported and called in code are already proven right and reliable.
4. You need to tell what specifically the user need to add or clarify to solve the problem.
5. What you ask the user to clarify must related to the database content we have.
6. What you ask must about user query input, do not ask user to provide data.
7. What you ask should be short and clear.
8. If any example input or default value for user to replace with actual data in code, problem not solved!!! Ask the user to provide information.
"""
    return question_prompt + code_prompt + ans_prompt + data_prompt + end_prompt


def get_ans_review(question: str, ans: str, code: str):
    prompt = get_ans_review_prompt(question, ans, code)
    ans = call_llm(prompt, llm)
    return ans.content
