import re

def insert_yield_statements(code):
    # 去除所有空行
    code = '\n'.join([line for line in code.split('\n') if line.strip()])
    # 使用正则表达式匹配赋值语句，考虑行首的空白字符
    assignment_pattern = re.compile(r'^(\s*)(\w+)\s*=\s', re.MULTILINE)
    # 使用正则表达式匹配yield语句，考虑行首的空白字符
    yield_pattern = re.compile(r'^(\s*)yield\s+(\w+)', re.MULTILINE)

    lines = code.split('\n')
    new_lines = []

    # 创建一个集合来跟踪已经yield过的变量
    yielded_variables = set()
    for i in range(len(lines)):
        line = lines[i]
        yield_match = yield_pattern.match(line)
        if yield_match:
            variable_name = yield_match.group(2)
            yielded_variables.add(variable_name)

    for i in range(len(lines)):
        line = lines[i]
        new_lines.append(line)

        # 检查当前行是否是赋值语句
        assignment_match = assignment_pattern.match(line)
        if assignment_match:
            indentation, variable_name = assignment_match.groups()
            # 检查下一行是否是yield该变量的语句
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                yield_match = yield_pattern.match(next_line)
                # 如果下一行不是yield该变量的语句，或者还没有yield过该变量
                if not yield_match or yield_match.group(2) != variable_name:
                    # 并且该变量还没有被yield过
                    if variable_name not in yielded_variables:
                        # 插入yield语句，保持相同的缩进
                        new_lines.append(f"{indentation}yield {variable_name}")
                        # 将变量添加到已yield的集合中
                        yielded_variables.add(variable_name)

        # 检查当前行是否是yield语句
        yield_match = yield_pattern.match(line)
        if yield_match:
            variable_name = yield_match.group(2)
            # 将变量添加到已yield的集合中
            yielded_variables.add(variable_name)

    return '\n'.join(new_lines)


def insert_lines_into_function(code_str: str, lines_to_insert: list) -> str:
    # 找到def func():的位置
    func_start_index = code_str.find('def func(')

    # 如果没有找到def func()，则返回原字符串
    if func_start_index == -1:
        return code_str
    # 找到def func()后的第一个换行符
    newline_index = code_str.find('\n', func_start_index)
    # 如果没有找到换行符，则返回原字符串
    if newline_index == -1:
        return code_str
    # 在换行符后添加换行符，为插入代码做准备
    code_str = code_str[:newline_index + 1] + '\n' + code_str[newline_index + 1:]
    # 插入每一行代码，每行代码前添加四个空格作为缩进
    for line in lines_to_insert:
        code_str = code_str[:newline_index + 2] + '    ' + line + '\n' + code_str[newline_index + 2:]
    return code_str


if __name__=="__main__":
    # 示例代码
    original_code = """
def func(data: pd):
    import pandas as pd
    from agent.tools.tools_def import query_database, draw_graph
    import math

    yield "正在查询LORONG 7 TOA PAYOH的位置信息..."
    toa_payoh_location = query_database("查询LORONG 7 TOA PAYOH的经纬度", "latitude, longitude")
    """
    lines_to_insert = ["import pandas as pd", "import math"]

    # 调用函数并打印结果
    modified_code = insert_lines_into_function(original_code, lines_to_insert)
    print(modified_code)

