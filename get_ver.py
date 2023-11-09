import tomllib

from pathlib import Path

with open(Path(__file__).parent / "pyproject.toml", mode="rb") as f:
    pyproject = tomllib.load(f)


print(pyproject["project"]["version"])
