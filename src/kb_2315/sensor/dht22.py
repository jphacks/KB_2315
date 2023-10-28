from dataclasses import dataclass


@dataclass
class dht22_data:
    temperature: float = 0.0
    humidity: float = 0.0
