from dataclasses import asdict
from pathlib import Path

import toml

from kb_2315.config.env import env


root_dir: Path = Path(__file__).parents[3]


def read_config(
    dir: Path = root_dir,
    name: str = "config.toml",
) -> env:
    file: Path = dir / name

    if not file.exists():
        write_config(config=env())
        raise FileNotFoundError(f"Config file {file} not found")
    else:
        with file.open() as f:
            return env(**toml.loads(f.read()))


def write_config(
    config: env,
    dir: Path = root_dir,
    name: str = "config.toml",
) -> None:
    file: Path = dir / name

    with file.open("w") as f:
        f.write(toml.dumps(asdict(config)))


conf: env = read_config()
