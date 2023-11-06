from random import random
from time import sleep

import requests

from kb_2315.backend.crud import crud_shoe
from kb_2315.backend.schemas import schema_sensor, schema_session
from kb_2315.config import conf


try:
    device_id: int = crud_shoe.search_shoe_by()[0].id
except IndexError:
    device_id = crud_shoe.add_shoe()


resp: schema_session.create_session = schema_session.create_session.model_validate(
    obj=requests.get(f"{conf.host_url}/session/?shoe_id={device_id}").json()
)

str_sesison_id = str(resp.session_id)

print(device_id, str_sesison_id)

it = 3

for i in range(it):
    requests.post(
        url=f"{conf.host_url}/sensor/",
        json=schema_sensor.sensor(
            session_id=str_sesison_id,
            device_id=device_id,
            external_temperature=random() * 30,
            external_humidity=random() * 100,
            internal_temperature=random() * 30,
            internal_humidity=random() * 100,
            drying=(i < it - 1),
        ).model_dump(),
    )

    sleep(2)
