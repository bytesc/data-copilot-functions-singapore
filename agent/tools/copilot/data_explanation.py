from .utils import call_llm_test

from .utils.parse_output import parse_generated_python_code

import logging
import pandas as pd

pd.set_option('display.max_columns', None)


def get_llm_data_explanation_func(question, data, llm, max_length=10000):
    data_str = data.to_string()
    if len(data_str) > max_length:
        sampling_ratio = max_length / len(data_str)
        n_rows = max(1, int(len(data) * sampling_ratio))
        sampled_data = data.sample(n=n_rows)
        data_str = sampled_data.to_string()

    pre_prompt = """
Please explain the data provided base on the data and question provided.
Here is the question:
"""

    data_prompt = """
Here is the dataframe: 
""" + data_str

    end_prompt = """
Remind:
1. Please analyze and explain the trends, patterns, and cycles in the data based on the question.
2. Please provide suggestions base on the question and data analysis.
3. The Answer should be short and clear, around 150 words is better.
4. Just describe the data, do not use any phrase to explain what you are doing.
"""

    final_prompt = pre_prompt + question + "\n" + data_prompt + end_prompt
    ans = call_llm_test.call_llm(final_prompt, llm)

    return ans.content

