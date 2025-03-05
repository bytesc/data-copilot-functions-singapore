import sqlalchemy
from sqlalchemy import create_engine
from .utils.call_llm_test import call_llm

engine = create_engine('sqlite:///api_backend/db.sqlite3')


def get_api_select_prompt(question:str):
    pre_prompt = """ 
    Please select the APIs need to use based on the question.
    You can select multiple APIs, to solve the problem.
    You can choose as many as possible to ensure that the problem can be solved.
    """
    function_prompt = """ 
    Here is the APIs you can use:
    """
    example_code = """
    Please only return the names list of the APIs split by ","
    If you think none of the APIs is helpful, return a single word: "no".
    
    Example 1:
    draw graph, query database
    Example 2:
    no
    """
    api_info_dict = {}
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
                        SELECT api_name, api_description FROM api_info WHERE api_group='Population Query'
                                            """),
                              {})
        conn.commit()
        api_info_result = result.fetchall()
        for api_name, api_description in api_info_result:
            api_info_dict[api_name] = api_description
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()

    return "question: "+question+pre_prompt+function_prompt+str(api_info_dict)+example_code


def get_population_api_info(question: str, llm):
    api_select_prompt = get_api_select_prompt(question)
    api_list_str = call_llm(api_select_prompt, llm).content
    api_list = [part.strip() for part in api_list_str.split(',')]
    placeholders = ', '.join("\'"+i+"\'" for i in api_list)

    api_detail_dict = {}
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text(f"""
                            SELECT api_name, api_description, api_url, api_docs FROM api_info WHERE api_name IN ({placeholders})
                                                """),
                              {})
        conn.commit()
        api_detail_result = result.fetchall()
        for api_name, api_description, api_url, api_docs in api_detail_result:
            api_detail_dict[api_name] = api_description+"\n"+api_url+"\n"+api_docs
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()
    return api_detail_dict

