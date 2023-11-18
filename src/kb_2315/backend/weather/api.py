import requests


def get_weather_code(ido_longitude: float, keido_latitude: float) -> int:
    url: str = (
        f"https://api.open-meteo.com/v1/forecast?latitude={ido_longitude}&longitude={keido_latitude}"
        "&timezone=Asia%2FTokyo&forecast_days&current=weather_code"
    )

    try:
        r = requests.get(url).json()
        return r.get("daily").get("weather_code")
    except Exception:
        # 困ったら曇り
        return 2
