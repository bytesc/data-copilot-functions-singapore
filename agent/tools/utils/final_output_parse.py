import re


def is_url(s):
    # 简单的URL正则表达式
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return re.match(url_regex, s) is not None


def wrap_url_with_markdown_image(url):
    return f"![image]({url})"


def is_png_url(s):
    # 修改正则表达式，使其可以匹配字符串中包含的URL，且URL以.png结尾
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.png'
    )
    # 使用findall来查找所有匹配的URL
    return len(re.findall(url_regex, s)) > 0


def wrap_png_url_with_markdown_image(s):
    # 使用正则表达式找到所有匹配的URL
    url_regex = re.compile(
        r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.png)'
    )
    # 替换找到的每个URL为Markdown格式的图片链接
    return re.sub(url_regex, r"![image](\1)", s)

import pandas as pd


def df_to_markdown(df, bold_header=False):
    # Start with the header
    header = df.columns.tolist()
    if bold_header:
        header = ["**{}**".format(col) for col in header]
    markdown_str = " | ".join(header) + " \n"

    # Add separator
    markdown_str += " | ".join(['---' for _ in header]) + " \n"

    # Add rows
    for index, row in df.iterrows():
        # Escape pipe characters in the cells
        escaped_row = [str(cell).replace("\n", "<br>").replace("|", "\\|") for cell in row]
        markdown_str += " | ".join(escaped_row) + " \n"

    return markdown_str+"\n"
