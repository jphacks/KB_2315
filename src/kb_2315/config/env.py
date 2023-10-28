from dataclasses import dataclass
from pathlib import Path

root_dir: Path = Path(__file__).parents[3]


@dataclass()
class env:
    client_ip: str = ""
