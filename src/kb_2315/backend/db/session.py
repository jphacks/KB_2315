from sqlalchemy import Engine, create_engine

import kb_2315.config as config


if config.conf.USE_EXTERNAL_DB:
    engine: Engine = create_engine(
        f"postgresql://{config.conf.DB_USER}:{config.conf.DB_PASSWORD}@{config.conf.DB_HOST}:{config.conf.DB_PORT}",
    )

else:
    engine = create_engine(
        f"sqlite:///{config.root_dir / 'db.sqlite3'}",
        connect_args={"check_same_thread": False},
    )
