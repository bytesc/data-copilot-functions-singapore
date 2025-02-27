from typing import List, Tuple, Optional


def get_minimap_func(lat_lng_list: Optional[List[Tuple[float, float]]] = None,
                postcode_list: Optional[List[str]] = None) -> str:
    # lat_lng_list = [
    #     (1.2996492424497, 103.8447478575),
    #     (1.29963489170907, 103.845842317726),
    #     # 可以继续添加更多经纬度
    # ]

    # postcode_list = ["123456",]
    print(lat_lng_list,postcode_list)

    # 基础字符串模板
    base_string = '<iframe src="https://www.onemap.gov.sg/amm/amm.html?mapStyle=Default&zoomLevel=15'

    # 遍历经纬度列表，添加标记
    if lat_lng_list:
        for lat, lng in lat_lng_list:
            base_string += f'&marker=latLng:{lat},{lng}!colour:red'

    if postcode_list:
        for postalcode in postcode_list:
            base_string += f'&marker=postalcode:{postalcode}!colour:red'

    # 添加iframe的其他属性
    base_string += '" height="450" width="450" scrolling="no" frameborder="0" allowfullscreen="allowfullscreen"></iframe>'

    # print(base_string)
    return base_string



