import requests
from engtoolslab2.config import config


def fetch_live_data():
    config.validate()

    url = "https://ipinfo.io/json"

    headers = {
        "Authorization": f"Bearer {config.api_key}"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    return {
        "status": "LIVE_SUCCESS",
        "ip": data.get("ip"),
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country"),
        "org": data.get("org"),
    }