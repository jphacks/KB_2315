from random import random
from time import sleep

import requests

from kb_2315.backend.schemas import schema_sensor, schema_session
from kb_2315.config import conf


device_id = 100


resp: schema_session.create_session = schema_session.create_session.model_validate(
    obj=requests.get(f"{conf.host_url}/api/session/?device_id={device_id}").json()
)

str_session_id = str(resp.session_id)

print(device_id, str_session_id)

it = 3

for i in range(it):
    requests.post(
        url=f"{conf.host_url}/api/sensor/",
        json=schema_sensor.sensor(
            session_id=str_session_id,
            device_id=device_id,
            external_temperature=random() * 30,
            external_humidity=random() * 100,
            internal_temperature=random() * 30,
            internal_humidity=random() * 100,
            drying=(i < it - 1),
        ).model_dump(),
    )

    sleep(2)
