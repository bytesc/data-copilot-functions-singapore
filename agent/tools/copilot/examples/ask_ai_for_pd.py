def get_ask_pd_prompt(question):
    pre_prompt = """ 
Please process the data based on the question.
The Python function should return a single pandas dataframe only!!! 
Do not save any thing. 
"""
    example_code = """
Here is an example: 
```python
def func(data):
    import pandas as pd
    import math
    # generate code to perform operations here
    return result
```
"""
    return "question:"+question + pre_prompt + example_code
