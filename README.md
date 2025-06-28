# data-copilot-functions-singapore


✨ **基于代码生成和函数调用(function call)的大语言模型(LLM)智能体**

基于人工智能的数据分析助力新加坡房地产、教育及城市规划更智能决策。Data-Copilot 是一款面向垂直领域的综合智能数据解决方案。
它不仅超越了简单的自然语言转SQL（NL2SQL）工具或基础智能体框架，更将领域专业知识、结构化数据处理与AI驱动的决策支持深度融合，打造出统一的全栈式系统。

通过自然语言提问，使用大语言模型智能解析数据库结构，对数据进行智能多表结构化查询和统计计算，根据查询结果智能绘制多种图表。
支持自定义函数(function call)和Agent调用，多智能体协同。
基于代码生成的思维链(COT)。 实现智能体对用户的反问，解决用户提问模糊、不完整的情况。

🚩[English Readme](./README.en.md)

### 相关项目
- [基于大语言模型 (LLM) 的<u>**可解释型**</u>自然语言数据库查询系统 https://github.com/bytesc/data-copilot-steps](https://github.com/bytesc/data-copilot-steps)
- [基于大语言模型 (LLM)和并发预测模型的自然语言数据库查询系统 (https://github.com/bytesc/data-copilot-v2](https://github.com/bytesc/data-copilot-v2)

[个人网站：www.bytesc.top](http://www.bytesc.top)

🔔 如有项目相关问题，欢迎在本项目提出`issue`，我一般会在 24 小时内回复。

## 功能简介

- 1, 基于代码生成的大语言模型智能体(AI Agent)。
- 2, 实现智能体对用户的反问，解决用户提问模糊、不完整的情况。
- 3, 智能体支持灵活的自定义函数调用(function call)和思维链(COT)
- 4, 实现多智能体的合作调用
- 5, 智能体实现智能绘制多种统计图表
- 6, 能够处理大语言模型表现不稳定等异常情况
- 7, 支持 `openai` 格式(如 `glm` ,`deepseek`, `qwen`)的 api 接口


- 1, 支持新加坡的地理信息数据库查询，包含新加坡的公共交通、HDB房产、学校和教育设施、邮编与区域划分等关键信息
- 2, 整合新加坡 OneMAP 的地图和数据 API。
- 3, 支持基于机器学习的新加坡房价预测模型。

## 需求分析

### 问题/痛点  
- **通用大语言模型缺乏领域特定数据**——无法支持垂直行业（房地产、教育、城市规划）的数据驱动决策。  
- **数据碎片化且杂乱无章**——专业人士需手动整理信息，浪费大量时间。  
- **幻觉与不可靠的输出**——现有智能体无法提供准确、结构化的分析。  
- **缺乏统一平台**——企业和政府依赖昂贵的一次性解决方案。  
- **示例**：现有大语言模型无法提供准确的近期二手房价格或交易量数据。  

![](./readme_static/pro.png)

### 目标受众与市场规模  
- **购房者与公众**——获取结构化房产/教育洞察，用于长期家庭规划（如购房、择校）、日常生活与交通、实时决策。  
- **房地产与教育行业专业人士**——基于AI的分析工具，为客户定制策略。  
- **政府与城市规划者**——数据驱动的政策制定：城市规划、设施选址与调度、交通优化。

## 创新点
- 基于代码生成的智能体(Agent)支持灵活的自定义函数调用(function call)和思维链(COT)
- 引入函数依赖图(Function Graph)的概念，实现自定义函数调用
- 引入智能体函数(Agent as Function)的概念，实现多智能体(Agent)的合作调用
- 实现智能体(Agent)对用户的反问，解决用户提问模糊、不完整的情况
- 包含输出断言和异常处理，能够处理大语言模型表现不稳定等异常情况

## 技术路线

### 解决方案概述

- **融合大语言模型与结构化数据**：提升决策能力，提供精准洞察。  
- **解决数据碎片化问题**：整合公共、行业及政府数据需求，打造统一平台。  
- **简化复杂查询**：基于知识图谱（Knowledge Graph）与上下文压缩（Context Compression）技术，高效解析多维度问题。  
- **优化用户交互**：通过提示词工程（Prompt Engineering）和思维链（Chain of Thought）技术，实现更自然的对话式分析。  
- **自动化代码生成**：针对多样化用户场景，快速生成定制化解决方案代码，提升开发效率。

![](./readme_static/struct.png)

### 核心组件与技术架构  

#### **1. 可配置的LLM主干模型**  
- 支持主流大模型（如GPT-4o、Claude等），灵活适配不同场景需求。  

#### **2. 动态工具调用的函数图谱（Function Graph）**  
- 智能选择最佳工具链，根据任务类型动态组合数据查询、分析与可视化功能。  

#### **3. 多智能体协作层**  
- 通过角色化Agent分工（如数据查询Agent、校验Agent、报告生成Agent）实现复杂任务流水线处理。  

#### **4. 深度垂直整合模块**  
- **地理空间数据API**（如新加坡OneMap）  
- **房价预测模型**（结合历史交易、区域发展等动态因子）

（注：架构设计强调领域适应性，例如房地产场景可快速扩展"租金收益率计算"等专属模块）

### AI agent

![](./readme_static/流程图1.png)

基本程序流水线图：

![](./readme_static/流程图2.png)


基本流程：
User query → Function selection → Code generation → Execution → Validation
1. **Question**: 用户自然语言问题提问
2. **Function Selection**: LLM 根据函数基本信息选择多个函数，通过函数依赖图(Function Graph)获得可用函数列表和详细注释（函数包括非智能体函数(Custum Function)和调用其它智能体的函数(Agent as Function)，实现多智能体协同）
3. **Function Calls Chain**: LLM 根据函数列表和详细注释，生成调用多个函数的 python 代码并执行
4. **Result Review**: LLM 回顾总结整个流程，评估问题是否解决，没有解决则反问用户，使其澄清问题或者提供更多信息


## 展示

### 演示

智能数据库查询、统计计算和绘图(Agent 协同)

![](./readme_static/r1.png)

地图标注(自定义function call)

![](./readme_static/r2.png)

智能绘图不满意，可以交互式绘图

![](./readme_static/r3.png)

用户提供信息不足以完成任务时，反问用户使其补充信息(Result Review)

![](./readme_static/r4.png)

### 原理

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
server_port: 8009 # 部署端口
server_host: "0.0.0.0"  # allow host
# 数据库
mysql: "mysql+pymysql://root:123456@localhost:3306/singapore_land"

# 静态文件服务地址，本机域名/ip:端口
static_path: "http://127.0.0.1:8009/"

model_name: "qwen-max"
# glm-4
# deepseek-chat
# qwen-max
# gpt-4o-mini

model_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
# https://open.bigmodel.cn/api/paas/v4/
# https://api.deepseek.com/v1/
# https://dashscope.aliyuncs.com/compatible-mode/v1
# https://api.openai.com/v1

```

### 大语言模型配置


新建文件：`agent\utils\llm_access\api_key_openai.txt` 在其中填写`api-key`

`api-key`获取链接：
- 阿里云:[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
- deepseek:[https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
- glm:[https://open.bigmodel.cn/](https://open.bigmodel.cn/)


### Onemap API

新建文件：`agent/tools/map/utils/onemap_email.txt` 在其中填写邮箱

新建文件：`agent/tools/map/utils/onemap_password.txt` 在其中填写密码

### 运行

#### 服务端

```bash
# 服务端
python ./main.py
```

#### 前端

如果以 dev 模式运行
修改`./vue-front/vite.config.js`

```javascript
export default defineConfig({
  plugins: [vue()],
  server:{
    port : 8086, //前端指定部署端口号
    proxy:{
      "/api":{  //后端地址
        target:"http://127.0.0.1:8009/"
      }
    }
  },
  base: "./" 
})
```

```bash
cd ./vue-front/
npm install
npm run dev
```

如果编译运行

```bash
cd ./vue-front/
npm run build
```

可以使用 nginx 等工具部署编译生成的 dist 文件夹

也可以使用 python 脚本部署

修改`./vue-front/front-server/front-server.py`
```python
BASE_URL = "http://127.0.0.1:8009" # 后端地址
HOST = "0.0.0.0" # 前端 allow host
PORT = 8086 # 前端 端口号
```

```bash
# 启动前端服务
cd ./vue-front/front-server/
python front-server.py
```


### 自定义 function call

在 `agent/tools/custom_tools_def.py` 中定义自定义函数

需要写规范、详细的注释，前三行是函数基本功能信息，之后是详细信息

例子：

```python
from typing import List, Tuple, Optional
from .map.get_onemap_minimap import get_minimap_func

def get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None,
                postcode_list: Optional[List[str]] = None) -> str:
    """
    get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None, postcode_list: Optional[List[str]] = None) -> str:
    Generate an HTML iframe for a minimap with optional markers in latitude and longitude pairs or or postal codes.
    Returns an HTML iframe string.

    The function creates an HTML iframe that embeds a minimap from OneMap.sg.
    Users can specify a list of latitude and longitude pairs or postal codes
    to be marked on the map.

    Args:
    - lat_lng_list (Optional[List[Tuple[float, float]]]): A list of tuples,
      where each tuple contains a latitude and longitude pair for a marker.
      Default is None.
    - postcode_list (Optional[List[str]]): A list of postal codes to be marked
      on the map. Default is None.

    Returns:
    - str: An HTML iframe string that can be embedded in a webpage to display
      the minimap with the specified markers.

    Example usage:
    ```python
    get_minimap_func(lat_lng_list=[(1.2996492424497, 103.8447478575), (1.29963489170907, 103.845842317726)])
    get_minimap_func(postcode_list=["123456"])
    ```

    """
    html = get_minimap_func(lat_lng_list, postcode_list)
    return html
```

然后在 `agent/tools/get_function_info.py` 中注册函数

import 函数之后，在 `FUNCTION_DICT` 中添加函数，在 `FUNCTION_IMPORT ` 中添加 import 语句

例如：

```python
from .custom_tools_def import get_minimap  # 导入


FUNCTION_DICT = {
    "query_database": query_database,
    "draw_graph": draw_graph,
    "get_minimap": get_minimap   # 注册
}

FUNCTION_IMPORT = {
    query_database: "from agent.tools.tools_def import query_database",
    draw_graph: "from agent.tools.tools_def import draw_graph",
    get_minimap: "from agent.tools.custom_tools_def import get_minimap"  # 添加 import
}
```

`ASSIST_FUNCTION_DICT` 定义了函数的依赖关系图。

例如：

```python
ASSIST_FUNCTION_DICT = {
    # predict_grade_for_stu: [from_username_to_uid, from_lesson_name_to_lesson_num],
}
```

# 开源许可证

此翻译版本仅供参考，以 LICENSE 文件中的英文版本为准

MIT 开源许可证：

版权所有 (c) 2025 bytesc

特此授权，免费向任何获得本软件及相关文档文件（以下简称“软件”）副本的人提供使用、复制、修改、合并、出版、发行、再许可和/或销售软件的权利，但须遵守以下条件：

上述版权声明和本许可声明应包含在所有副本或实质性部分中。

本软件按“原样”提供，不作任何明示或暗示的保证，包括但不限于适销性、特定用途适用性和非侵权性。在任何情况下，作者或版权持有人均不对因使用本软件而产生的任何索赔、损害或其他责任负责，无论是在合同、侵权或其他方面。
