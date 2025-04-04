import mimetypes

import sqlalchemy
import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse


from utils.get_config import config_data

from agent.agent import cot_agent
from agent.summary import get_ans_summary

# DATABASE_URL = config_data['mysql']
# engine = sqlalchemy.create_engine(DATABASE_URL)

app = FastAPI()

STATIC_FOLDER = "tmp_imgs"
STATIC_PATH = f"/{STATIC_FOLDER}"
# http://127.0.0.1:8003/tmp_imgs/mlkjcvep.png
@app.get(f"/{STATIC_FOLDER}/{{filename}}")
async def read_static_file(request: Request, filename: str):
    filepath = os.path.join(STATIC_FOLDER, filename)
    if os.path.isfile(filepath):
        # 猜测文件的MIME类型
        content_type, _ = mimetypes.guess_type(filepath)
        if content_type is None:
            content_type = "application/octet-stream"  # 默认为二进制流，如果无法确定类型
        # 读取文件内容
        with open(filepath, "rb") as file:
            file_content = file.read()
        # 返回Response对象，文件内容作为字节流发送
        return Response(content=file_content, media_type=content_type)
    else:
        return {"error": "File not found"}


class AgentInput(BaseModel):
    question: str


@app.post("/api/ask-agent/")
async def ask_agent(request: Request, user_input: AgentInput):
    ans, map = cot_agent(user_input.question)
    print(ans)
    if ans:
        processed_data = {
            "question": user_input.question,
            "ans": ans,
            "map": map,
            "type": "success",
            "msg": "处理成功"
        }
    else:
        processed_data = {
            "question": user_input.question,
            "ans": "",
            "map": "",
            "type": "error",
            "msg": "处理失败，请换个问法吧"
        }
    return JSONResponse(content=processed_data)


@app.post("/api/agent-summary/")
async def agent_summary(request: Request, user_input: AgentInput):
    ans = get_ans_summary(user_input.question)
    print(ans)
    if ans:
        processed_data = {
            "question": user_input.question,
            "ans": ans,
            "type": "success",
            "msg": "处理成功"
        }
    else:
        processed_data = {
            "question": user_input.question,
            "ans": "",
            "type": "error",
            "msg": "处理失败，请换个问法吧"
        }
    return JSONResponse(content=processed_data)


if __name__ == "__main__":
    uvicorn.run(app, host=config_data['server_host'], port=config_data['server_port'])
