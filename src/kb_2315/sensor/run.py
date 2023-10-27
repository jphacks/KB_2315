import kb_2315.config as config

import requests

from kb_2315.sensor.dht22 import dht22_data

url: str = f"http://{config.read_config(dir=config.root_dir).client_ip}/data"
response = requests.get(url)

d = dht22_data(**response.json())
print(d)
