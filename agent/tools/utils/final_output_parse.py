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
    url_regex = re.compile(
        r'http[s]?://[^"]+\.(?:png)'
    )
    return len(re.findall(url_regex, s)) > 0


def wrap_png_url_with_markdown_image(s):
    url_regex = re.compile(
        r'(http[s]?://[^"]+\.(?:png))'
    )
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
