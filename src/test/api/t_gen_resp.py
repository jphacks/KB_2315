from time import sleep

import requests

from kb_2315.api import schemas


import kb_2315.config as config
conf: config.env = config.read_config(dir=config.root_dir)


requests.post(
    url=conf.host_url,
    json=schemas.machine(id=1, status={"オキニのやつ": False}).model_dump(),
)

sleep(2)

requests.post(
    url=conf.host_url,
    json=schemas.machine(id=1, status={"オキニのやつ": True}).model_dump(),
)

sleep(2)

requests.post(
    url=conf.host_url,
    json=schemas.machine(id=1, status={"オキニのやつ": False}).model_dump(),
)
