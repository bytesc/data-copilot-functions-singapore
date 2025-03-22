import httpx
from utils.get_config import config_data

from pywebio.input import input, TEXT, textarea
from pywebio.output import put_text, put_html, put_markdown, clear, put_loading
from pywebio import start_server


def ai_agent_api(question: str, path: str = "/ask-agent/", url="http://127.0.0.1:" + str(config_data["server_port"])):
    # 使用 httpx 发送请求到另一个服务器的 /ask-agent/ 接口
    with httpx.Client(timeout=180.0) as client:
        try:
            response = client.post(url+path, json={"question": question})
            # 检查响应状态码
            if response.status_code == 200:
                print(response.json()["ans"])
                return response.json()["ans"]
            else:
                return None
        except httpx.RequestError as e:
            print(e)
            # 处理请求错误
            return None


def main():
    ans = None
    question_list = ""
    while 1:
        # put_text("Ask your question to the AI Agent:")
        question = textarea("Enter your question here:", type=TEXT, rows=2)
        put_markdown("## " + question)
        question_list = question_list + question

        req = question
        if ans:
            with put_loading():
                response = ai_agent_api(ans, "/agent-summary/")
                summary = response
                put_markdown("## Ans Summary")
                put_markdown(summary, sanitize=False)
                req = question_list + """
                This is the summary of the last conversation:
                            """ + summary

        with put_loading():
            print(req)
            response = ai_agent_api(req, "/ask-agent/")
            ans = response
        # print(response)
        # 检查响应并显示结果
        if response:
            put_markdown(response, sanitize=False)
        else:
            put_text("Failed to get a response from the AI Agent.")


# 启动 PyWebIO 应用
if __name__ == '__main__':
    start_server(main, port=8010)
