from dataclasses import dataclass


@dataclass()
class env:
    line_channel_access_token: str = ""
    line_channel_secret: str = ""
    line_group_id: str = ""
    host_url: str = ""

    USE_EXTERNAL_DB: bool = False
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_HOST: str = "db"
    DB_PORT: int = 5432
