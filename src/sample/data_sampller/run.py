import csv
from datetime import datetime
from time import sleep

import requests

import kb_2315.config as config
from kb_2315.csv.io import create_csv
from kb_2315.sensor.dht22 import dht22_data


url: str = f"http://{config.read_config(dir=config.root_dir).client_ip}/data"

with open(create_csv(), "w") as f:
    writer = csv.writer(f)
    response = requests.get(url)

    d = response.json()

    dh: list[dht22_data] = []

    val: list[datetime | float] = [datetime.now()]

    for k, v in d.items():
        if "sensor" in k:
            dh.append(dht22_data(**v))

    for d in dh:
        val.append(d.temperature)
        val.append(d.humidity)

    print(dh)

    writer.writerow(val)
    sleep(30)
