import uuid
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .logs import get_logger

logger = get_logger(__name__)


class Meta:
    version = uuid.uuid4()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Meta.version = uuid.uuid4()
    yield


def get_version() -> str:
    return str(Meta.version)


ROOT_DIR = Path(__file__).parent
app = FastAPI(
    title="App",
    lifespan=lifespan,
)
templates = Jinja2Templates(directory=ROOT_DIR / "templates")
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
    )


@app.websocket("/keep-alive")
async def keep_alive(websocket: WebSocket) -> None:
    await websocket.accept()
    logger.info("keep-alive client connected")
    try:
        while True:
            data = await websocket.receive_text()
            logger.error(f"Received keep-alive message: {data}")
    except WebSocketDisconnect:
        return


def serve():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_includes=["*.jinja2", "*.css"],
    )


if __name__ == "__main__":
    serve()
