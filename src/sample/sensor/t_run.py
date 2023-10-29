import requests

import kb_2315.config as config
from kb_2315.sensor.dht22 import dht22_data


url: str = f"http://{config.read_config(dir=config.root_dir).client_ip}/data"
response = requests.get(url)

d = response.json()

dh: list[dht22_data] = []

for k, v in d.items():
    if "sensor" in k:
        dh.append(dht22_data(**v))

print(dh)
