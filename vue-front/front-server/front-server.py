from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
import httpx
from httpx import Timeout

# 全局配置
BASE_URL = "http://127.0.0.1:8009"
HOST = "0.0.0.0"
PORT = 8086
# 设置10分钟超时
TIMEOUT = Timeout(10.0 * 60)  # 10 minutes

app = FastAPI()


# 代理解决跨域
@app.api_route("/api/{path:path}", methods=["GET", "POST"])
async def proxy(path: str, request: Request):
    # 确保转发时保留/api/路径
    url = f"{BASE_URL}/api/{path}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length"]}

    # 获取请求体
    body = await request.body()

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        if request.method == "GET":
            resp = await client.get(url, headers=headers)
        elif request.method == "POST":
            resp = await client.post(url, headers=headers, content=body)

        # 创建一个Response对象，包含原始内容、状态码和头部
        return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)


# 服务于首页
@app.get("/")
async def serve_index():
    return FileResponse('../dist/index.html')


# 服务于其他静态文件
@app.get("/{path:path}")
async def serve_static(path: str):
    return FileResponse(f'../dist/{path}')


@app.post("/")
async def serve_index_post():
    return FileResponse('../dist/index.html')


# 服务于其他静态文件
@app.post("/{path:path}")
async def serve_static_post(path: str):
    return FileResponse(f'../dist/{path}')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
