import uvicorn
from fastapi import FastAPI, Request  # noqa

import kb_2315.config as config
from kb_2315.backend.api.router import api_router
from kb_2315.notify import line_rich_menu


conf: config.env = config.read_config(dir=config.root_dir)

app = FastAPI(
    root_path="/api",
)
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    line_rich_menu.create_rich_menu()

    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8888,
            host="0.0.0.0",
            root_path="/api",
        )
    )
    server.run()
