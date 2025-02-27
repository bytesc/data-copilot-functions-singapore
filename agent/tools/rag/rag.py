
from .utils.call_llm_test import call_llm




def get_rag_summarize_prompt(question: str, vector_db_ans: str):
    pre_prompt = """
This is the information from search:
"""
    question_prompt = """
Please summarize it to provide information related to the question:
"""
    end_prompt = """
Remind:
1. Do not try to answer question or solve the problem, just provide some information.
2. Do not mention what you do not know, just provide the information you already know. 
3. Please indicate the source of the content you cite from.
4. If you did not find any useful information, just tell me no useful information in knowledge base, 
do not explain or ask for more information.
"""
    return pre_prompt + str(vector_db_ans) + question_prompt + question + end_prompt


def get_rag_split_prompt(question: str):
    pre_prompt = """
You need to generate some key words and phrases based on the question provided. 
These sentences and phrases will be used as the input of an RAG(Retrieval-Augmented Generation) system.
"""
    question_prompt = """
Here is the question:
"""
    end_prompt = """
Remind:
1. Please only return the sentences and phrases list split by ","
2. RAG(Retrieval-Augmented Generation) system is not database, you should try to find base knowledge information.
3. Do not add any explanations of commands!!!

Example 1:
score to GPA, graduation requirement
Example 2:
地区房价情况, 学区房分布, 地区交通规划
"""
    return pre_prompt + question_prompt + question + end_prompt


def rag_from_policy_func(question: str, llm, engine):
    question_list_str = call_llm(get_rag_split_prompt(question), llm).content
    question_list = [part.strip() for part in question_list_str.split(',')]
    question_list.append(question)
    question_list = [question, ]
    # vector_db_ans = get_from_vector_db(question_list, 10, MODEL_PATH, engine)
    # # print(vector_db_ans)
    # # print(ans.shape[0])
    #
    # ans = call_llm(get_rag_summarize_prompt(question, vector_db_ans), llm)
    # return ans.content
    return None
