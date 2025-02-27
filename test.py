import httpx
from utils.get_config import config_data

from pywebio.input import input, TEXT
from pywebio.output import put_text, put_html, put_markdown
from pywebio import start_server

def ai_agent_api(question: str, url="http://127.0.0.1:"+str(config_data["server_port"])+"/ask-agent/"):
    # 使用 httpx 发送请求到另一个服务器的 /ask-agent/ 接口
    with httpx.Client(timeout=180.0) as client:
        try:
            response = client.post(url, json={"question": question})
            # 检查响应状态码
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except httpx.RequestError as e:
            print(e)
            # 处理请求错误
            return None


def main():
    put_text("Ask your question to the AI Agent:")
    question = input("Enter your question here:", type=TEXT)

    # 调用 AI Agent API
    response = ai_agent_api(question)
    # print(response)

    # 检查响应并显示结果
    if response:
        # 假设响应是一个字典，并且包含一个 'answer' 键
        put_markdown(response)
    else:
        put_text("Failed to get a response from the AI Agent.")


# 启动 PyWebIO 应用
if __name__ == '__main__':
    start_server(main, port=8080)
