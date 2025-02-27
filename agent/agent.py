import pandas as pd

from .tools.tools_def import engine, llm

from .tools.copilot.python_code import get_py_code
from .tools.copilot.utils.code_executor import execute_py_code
from .tools.copilot.sql_code import get_db_info_prompt

from .utils.code_insert import insert_lines_into_function
from .tools.get_function_info import get_function_info

from .ans_review import get_ans_review
from .utils.final_output_parse import df_to_markdown, wrap_html_url_with_markdown_link, wrap_html_url_with_html_a
from .utils.final_output_parse import wrap_png_url_with_markdown_image,is_png_url
from .utils.pd_to_walker import pd_to_walker

IMPORTANT_MODULE = ["import pandas as pd", "import math", "import numpy as np"]


def get_cot_prompt(question):
    data_prompt = get_db_info_prompt(engine, simple=True)
    # rag_ans = rag_from_policy_func(question,llm,engine)
    rag_ans = ""
    # print(rag_ans)

    question += "\nBase knowledge: \n" + rag_ans + "\n"
    question += "\nThe database content: \n" + data_prompt + "\n"

    function_info, function_import = get_function_info(question, llm)
    # print(function_info)
    if function_info == "solved":
        return "solved", rag_ans

    pre_prompt = """ 
Please use the following functions to solve the problem.
Please yield explanation string of each step as kind of report!
Please yield some information string during the function!
Please yield the result of each step and function call!
Please yield report many times during the function!!! not only yield at last! 
None or empty DataFrame return handling for each function call is extremely important.
"""
    function_prompt = """ 
Here is the functions you can import and use:
"""
    example_code = """
Here is an example: 
```python
def func():
    import pandas as pd
    import math
    # generate code to perform operations here
                
    yield "某班级的成绩如下："  # yield some information and explanation
    df = query_database("某班级的成绩", "姓名, 课程名, 成绩")   
    yield df  # the result of each step and function call
    # None or empty DataFrame return handling for each function call.
    if df == None:
        yield "数据库里没找到这个班级的成绩"
    else:
        yield "成绩柱状图如下："
        path = draw_graph("画柱状图", df)
        yield path
```
"""
    cot_prompt = "question:" + question + pre_prompt + \
                 function_prompt + str(function_info) + \
                 example_code
    return cot_prompt, rag_ans, function_import


def cot_agent(question, retries=2, print_rows=10):
    exp = None
    for i in range(3):
        cot_prompt, rag_ans, function_import = get_cot_prompt(question)
        print(rag_ans)
        # print(cot_prompt)
        if cot_prompt == "solved":
            return rag_ans
        else:
            err_msg = ""
            for j in range(retries):
                code = get_py_code(cot_prompt + err_msg, llm)
                # print(code)
                # code = insert_yield_statements(code)
                code = insert_lines_into_function(code, function_import)
                code = insert_lines_into_function(code, IMPORTANT_MODULE)
                print(code)
                if code is None:
                    continue
                try:
                    result = execute_py_code(code)
                    cot_ans = ""
                    for item in result:
                        # print(item)
                        if isinstance(item, pd.DataFrame):
                            if item.index.size > 10:
                                cot_ans += df_to_markdown(item.head(print_rows)) + \
                                           "\nfirst {} rows of {}\n".format(print_rows, len(item))
                            else:
                                cot_ans += df_to_markdown(item)
                            html_link = pd_to_walker(item)
                            # cot_ans += wrap_html_url_with_markdown_link(html_link)
                            cot_ans += wrap_html_url_with_html_a(html_link)
                        elif isinstance(item, str) and is_png_url(item):
                            cot_ans += "\n" + wrap_png_url_with_markdown_image(item) + "\n"
                        else:
                            cot_ans += "\n" + str(item) + "\n"
                        print(item)

                    ans = "### Base knowledge: \n" + rag_ans + "\n\n"
                    ans += "### COT Result: \n" + cot_ans + "\n"
                    # print(ans)
                    review_ans = get_ans_review(question, ans, code)
                    ans += "## Summarize and review: \n" + review_ans + "\n"
                    return ans
                except Exception as e:
                    err_msg = str(e) + "\n```python\n" + code + "\n```\n"
                    exp = e
                    print(e)
                    continue
    return None
