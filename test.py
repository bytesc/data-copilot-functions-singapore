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

    put_markdown("""
查询房价最高的10个房子的位置

获取到的数据如下：
blk_no | street | resale_price | PostCode
--- | --- | --- | ---
269A | PUNGGOL FIELD | 1228000 | 821269
267B | PUNGGOL FIELD | 1223880 | 822267
268B | PUNGGOL FIELD | 1220000 | 822268
268C | PUNGGOL FIELD | 1198000 | 823268
270C | PUNGGOL FIELD | 1150000 | 823270
267A | PUNGGOL FIELD | 1100888 | 821267
104 | LENGKONG TIGA | 1080000 | 410104
104 | LENGKONG TIGA | 1060000 | 410104
264 | TOA PAYOH EAST | 1059000 | 310264
261 | TOA PAYOH EAST | 1056500 | 310261

根据邮政编码生成地图


    """
                 ,sanitize=False)


# 启动 PyWebIO 应用
if __name__ == '__main__':
    start_server(main, port=8089)

