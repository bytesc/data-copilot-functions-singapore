from .parse_output import assert_skip

from agent.tools.tools_def import * #保留这一行，没错


def execute_py_code_with_data(code, data, assert_func=assert_skip):
    """
    执行生成的代码并返回结果。

    :param code: 生成的Python代码
    :param data: 输入数据
    :param assert_func: 断言函数，用于验证结果
    :return: 执行结果，如果执行成功且通过断言则返回结果，否则返回None
    """
    try:
        local_namespace = {'data': data, 'result': None}
        exec(code, globals(), local_namespace)
        result = local_namespace['func'](data)
        assert_result = assert_func(result)
        if assert_result:
            raise Exception(assert_result)
        return result
    except Exception as e:
        print(f"An error occurred while executing the code: {type(e).__name__}: {str(e)}")
        raise e


def execute_py_code(code, assert_func=assert_skip):
    """
    执行生成的代码并返回结果。

    :param code: 生成的Python代码
    :param assert_func: 断言函数，用于验证结果
    :return: 执行结果，如果执行成功且通过断言则返回结果，否则返回None
    """
    try:
        local_namespace = {'result': None}
        exec(code, globals(), local_namespace)
        result = local_namespace['func']()
        assert_result = assert_func(result)
        if assert_result:
            raise Exception(assert_result)
        return result
    except Exception as e:
        print(f"An error occurred while executing the code: {type(e).__name__}: {str(e)}")
        raise e
