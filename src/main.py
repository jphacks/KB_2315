import uvicorn
from fastapi import FastAPI

import kb_2315.config as config
from kb_2315.backend.api.router import api_router


conf: config.env = config.read_config(dir=config.root_dir)

app = FastAPI(root_path="/api")
app.include_router(api_router)


if __name__ == "__main__":
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8888,
            host="0.0.0.0",
        )
    )
    server.run()
