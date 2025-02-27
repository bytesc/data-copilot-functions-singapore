
from .tools_def import draw_graph, query_database
from .copilot.utils.call_llm_test import call_llm

FUNCTION_DICT = {
    "query_database": query_database,
    "draw_graph": draw_graph,
}
ASSIST_FUNCTION_DICT = {

}

IMPORTANT_FUNC = ["query_database"]

# FUNCTION_INFO = {key: func.__doc__ for key, func in FUNCTION_DICT.items()}
# ASSIST_FUNCTION_INFO = {key: ' '.join(func.__doc__ for func in funcs) for key, funcs in ASSIST_FUNCTION_DICT.items()}

FUNCTION_DESCRIPTION = {
    key: '\n'.join(func.__doc__.splitlines()[1:4]) for key, func in FUNCTION_DICT.items()
}


def get_function_prompt(question):
    # print(predict_grade_for_stu.__doc__)
    # print('\n'.join(predict_grade_for_stu.__doc__.splitlines()[1:3]))
    pre_prompt = """ 
Please select the functions need to use based on the question.
You can select multiple functions, to solve the problem.
You can choose as many as possible to ensure that the problem can be solved.
"""
    function_prompt = """ 
Here is the functions you can use:
"""
    example_code = """
Please only return the names list of the functions split by ","
If you think the question is already solved by Base Knowledge, return a single word: "solved".
Do not add any explanations of commands!!!

Example 1:
draw_graph, query_database
Example 2:
solved
"""
    return "question:" + question + pre_prompt + function_prompt + str(FUNCTION_DESCRIPTION) + example_code


def get_function_info(question, llm):
    function_prompt = get_function_prompt(question)
    function_list_str = call_llm(function_prompt, llm).content
    if function_list_str == "solved":
        return "solved"
    function_list = [part.strip() for part in function_list_str.split(',')]
    for f in IMPORTANT_FUNC:
        if f not in function_list:
            function_list.append(f)
    function_set = set()
    for function_name in function_list:
        # print(function_name)
        function = FUNCTION_DICT.get(function_name)
        if function:
            function_set.add(function)
            assist_functions = ASSIST_FUNCTION_DICT.get(function)
            if assist_functions:
                for assist_function in assist_functions:
                    function_set.add(assist_function)
    function_info = ""
    for function in function_set:
        function_info += "\n" + str(function.__doc__) + "\n"
    return function_info
