from .copilot.utils.call_llm_test import call_llm
from .tools_def import draw_graph, query_database
from .custom_tools_def import get_minimap, get_api_result, house_price_prediction_model, find_schools_near_postcode


FUNCTION_DICT = {
    "query_database": query_database,
    "draw_graph": draw_graph,
    "get_minimap": get_minimap,
    "get_api_result": get_api_result,
    "house_price_prediction_model": house_price_prediction_model,
    "find_schools_near_postcode": find_schools_near_postcode,
}

FUNCTION_IMPORT = {
    query_database: "from agent.tools.tools_def import query_database",
    draw_graph: "from agent.tools.tools_def import draw_graph",
    get_minimap: "from agent.tools.custom_tools_def import get_minimap",
    get_api_result: "from agent.tools.custom_tools_def import get_api_result",
    house_price_prediction_model: "from agent.tools.custom_tools_def import house_price_prediction_model",
    find_schools_near_postcode: "from agent.tools.custom_tools_def import find_schools_near_postcode",
}

ASSIST_FUNCTION_DICT = {
    # predict_grade_for_stu: [from_username_to_uid, from_lesson_name_to_lesson_num],
}

IMPORTANT_FUNC = ["query_database", "get_api_result"]

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
Do not add any explanations of commands!!!

Example 1:
draw_graph, query_database
"""
    return "question:" + question + pre_prompt + function_prompt + str(FUNCTION_DESCRIPTION) + example_code


def get_function_info(question, llm):
    function_prompt = get_function_prompt(question)
    function_list_str = call_llm(function_prompt, llm).content
    if function_list_str == "solved":
        return {}, "solved", []
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
    function_import = []
    for function in function_set:
        function_info += "\n" + str(function.__doc__) + "\n"
        import_list = FUNCTION_IMPORT.get(function)
        if import_list:
            function_import.append(import_list)
    return function_set, function_info, function_import
