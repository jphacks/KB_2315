def weather_code2icon(weather_code: int) -> str:
    """
    WMO 天気コードを4分類にする
    https://open-meteo.com/en/docs
    https://www.jodc.go.jp/data_format/weather-code_j.html#:~:text=%E7%8F%BE%E5%9C%A8%E5%A4%A9%E5%80%99(Present%20Weather)%20(WMO%20Code%204677)
    """
    if weather_code in [0, 1]:
        # 晴れ
        return "☀"

    elif weather_code in [2, 3]:
        # 曇り
        return "☁"

    elif weather_code in [
        # 雨
        45,
        48,
        51,
        53,
        55,
        56,
        57,
        61,
        63,
        65,
        66,
        67,
        80,
        81,
        82,
        95,
        96,
        99,
    ]:
        return "🌧"

    elif weather_code in [71, 73, 75, 77, 85, 86]:
        # 雪
        return "🌨"

    # その他
    else:
        # その他，曇りとする
        return "☁"
