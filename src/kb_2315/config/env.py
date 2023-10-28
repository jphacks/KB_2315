from dataclasses import dataclass
from pathlib import Path

root_dir: Path = Path(__file__).parents[3]


@dataclass()
class env:
    client_ip: str = ""
    line_channel_access_token: str = ""
    line_channel_secret: str = ""
