# smart class


✨ **基于代码生成和函数调用(function call)的大语言模型(LLM)智能体**

通过自然语言提问，使用大语言模型智能解析数据库结构，对数据进行智能多表结构化查询和统计计算，根据查询结果智能绘制多种图表。
支持自定义函数(function call)和Agent调用，多智能体协同。
基于代码生成的思维链(COT)。
实现智能体对用户的反问，解决用户提问模糊、不完整的情况。
Pywebio 交互式前端网页，不必须 openai api，100%纯 Python 代码。

🚩[English Readme](./README.en.md)

- [基于大语言模型 (LLM) 的<u>**可解释型**</u>自然语言数据库查询系统 (RAG) https://github.com/bytesc/data-copilot-steps](https://github.com/bytesc/data-copilot-steps)
- [基于大语言模型 (LLM)和并发预测模型的自然语言数据库查询系统 (RAG) (https://github.com/bytesc/data-copilot-v2](https://github.com/bytesc/data-copilot-v2)

🔔 如有项目相关问题，欢迎在本项目提出`issue`，我一般会在 24 小时内回复。

## 功能简介

- 1, 基于代码生成的大语言模型智能体(AI Agent)。
- 2, 实现智能体对用户的反问，解决用户提问模糊、不完整的情况。
- 3, 智能体支持灵活的自定义函数调用(function call)和思维链(COT)
- 4, 实现多智能体的合作调用
- 5, 智能体实现智能绘制多种统计图表
- 6, 智能体实现基于机器学习的智能成绩预测 
- 7, 能够处理大语言模型表现不稳定等异常情况
- 8, 支持 `openai` 格式(如 `glm` ,`deepseek`, `qwen`)的 api 接口


## 创新点
- 1, 实现智能体(Agent)对用户的反问，解决用户提问模糊、不完整的情况
- 2, 基于代码生成的智能体(Agent)支持灵活的自定义函数调用(function call)和思维链(COT)
- 3, 实现多智能体(Agent)的合作调用
- 4, 包含输出断言和异常处理，能够处理大语言模型表现不稳定等异常情况

## 技术路线

### AI agent 

基本程序流水线图：

![](./readme_static/流程图.png)

基本流程：
1. **Qusetion**: 用户自然语言问题提问
2. **RAG**: 通过检索增强生成(RAG)获取背景知识
3. **Function Selection**: LLM 根据函数基本信息选择多个函数，通过函数依赖图(Function Graph)获得可用函数列表和详细注释（函数包括非智能体函数(Custum Function)和调用其它智能体的函数(Agent as Function)，实现多智能体协同）
4. **Function Calls Chain**: LLM 根据函数列表和详细注释，生成调用多个函数的 python 代码并执行
5. **Result Review**: LLM 回顾总结整个流程，评估问题是否解决，没有解决则反问用户，使其澄清问题或者提供更多信息


## 展示

函数调用链(Function Call Chain)和智能体函数(Agent as Function)，实现多智能体协同原理示例

![](./readme_static/f1.png)

函数依赖图(Function Graph)和非智能体函数(Custom Functions)原理示例

![](./readme_static/f2.png)


## 如何使用

### 安装依赖

python 版本 3.10

```bash
pip install -r requirement.txt
```

### 配置文件

`config.yaml`
```yml
# config
server_port: 8003
server_host: "0.0.0.0"
# 填写数据库连接
mysql: "mysql+pymysql://root:123456@localhost:3306/smart_class2"

static_path: "http://127.0.0.1:8003/"
```

### 大语言模型配置

`agent\utils\llm_access\`文件夹包含大语言模型配置

`agent\utils\llm_access\LLM.py` 填写大语言模型(LLM)链接
```python
def get_llm():
    # 此处填写大语言模型(LLM)链接
    llm = OpenAI(api_key=get_api_key_from_file("./agent/utils/llm_access/api_key_openai.txt"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    return llm
    # https://open.bigmodel.cn/api/paas/v4/
    # https://api.deepseek.com/v1/
    # https://dashscope.aliyuncs.com/compatible-mode/v1
```

`agent\tools\copilot\utils\call_llm_test.py`和 `agent\tools\rag\utils\call_llm_test.py` 填写模型名称
```python
def call_llm(question, llm):
    response = llm.chat.completions.create(
        model="qwen-max",  # 此处填写模型名称
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    # glm-4
    # deepseek-chat
    # qwen-max
```

新建文件：`agent\utils\llm_access\api_key_openai.txt` 在其中填写`api-key`

`api-key`获取链接：
- 阿里云:[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
- deepseek:[https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
- glm:[https://open.bigmodel.cn/](https://open.bigmodel.cn/)



### 运行

```bash
# 服务端
python ./main.py
# 客户端
python ./front.py
```

# 开源许可证

此翻译版本仅供参考，以 LICENSE 文件中的英文版本为准

MIT 开源许可证：

版权所有 (c) 2025 bytesc

特此授权，免费向任何获得本软件及相关文档文件（以下简称“软件”）副本的人提供使用、复制、修改、合并、出版、发行、再许可和/或销售软件的权利，但须遵守以下条件：

上述版权声明和本许可声明应包含在所有副本或实质性部分中。

本软件按“原样”提供，不作任何明示或暗示的保证，包括但不限于适销性、特定用途适用性和非侵权性。在任何情况下，作者或版权持有人均不对因使用本软件而产生的任何索赔、损害或其他责任负责，无论是在合同、侵权或其他方面。
