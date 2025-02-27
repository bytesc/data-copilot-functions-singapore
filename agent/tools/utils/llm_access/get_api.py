# 从文件中读取API密钥
# ./llm_access/api_key.txt
def get_api_key_from_file(file_path='./agent/tools/utils/llm_access/api_key_openai.txt'):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

