from pywebio import start_server
from pywebio.output import put_markdown, put_html

from agent.tools.map.get_onemap_static_map import get_static_map

# get_static_map(1.31955, 103.84223, "static_map.png")
def main():
    put_markdown("""
    123
    <iframe src="https://www.onemap.gov.sg/amm/amm.html?mapStyle=Default&zoomLevel=15&marker=latLng:1.2996492424497,103.8447478575!colour:red&marker=latLng:1.29963489170907,103.845842317726!colour:red&marker=postalcode:238889!colour:red&popupWidth=200" height="450" width="450" scrolling="no" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
    456
    """
                 ,sanitize=False)


# 启动 PyWebIO 应用
if __name__ == '__main__':
    start_server(main, port=8089)

