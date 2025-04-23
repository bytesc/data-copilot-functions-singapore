from pywebio.input import input, TEXT, actions, textarea
from pywebio.output import put_html, put_text, put_table, put_markdown, put_image, put_code, put_loading, put_collapse, \
    toast, put_info
from pywebio import start_server

from agent.tools.copilot.utils.read_db import get_rows_from_all_tables
from agent.tools.tools_def import engine, llm


def main():
    put_markdown("# DATA COPILOT DB")
    first_five_rows = get_rows_from_all_tables(engine, None, num=5)
    # print(first_five_rows)
    with put_collapse(f"数据表："):
        for table_name, rows in first_five_rows.items():
            with put_collapse(f"表 {table_name}"):
                put_text(f"表 {table_name} 的前5行数据:")
                put_table([rows.columns.tolist()] + rows.values.tolist())


if __name__ == '__main__':
    start_server(main, port=8082)
