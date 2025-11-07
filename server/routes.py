from pathlib import Path

import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.params import Depends

from server.auth import get_user
from server.config import Config
from server.models import FileNode, FileNodeType, ListFilesResponse

files_router = APIRouter(
    prefix="/files",
    tags=["files"],
    dependencies=[Depends(get_user)],
)

DATA_DIR = Config.data_dir_path


@files_router.get("")
async def list_files() -> ListFilesResponse:
    files: list[FileNode] = []
    for file_path in DATA_DIR.glob("**/*"):
        relative = file_path.relative_to(DATA_DIR)

        file = FileNode(
            path=str(relative),
            type=FileNodeType.DIR if file_path.is_dir() else FileNodeType.FILE,
        )
        files.append(file)

    return ListFilesResponse(files=files)


@files_router.post("")
async def create_file(path: str, file: UploadFile) -> FileNode:
    if file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Missing file name"},
        )
    file_path = Path(path) / file.filename

    absolute_file_path = DATA_DIR / file_path

    if absolute_file_path.exists():
        message = "File already exists"
        raise HTTPException(status_code=400, detail={"message": message})

    absolute_file_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(absolute_file_path, "wb") as out:
        contents = await file.read()
        await out.write(contents)

    return FileNode(path=str(file_path), type=FileNodeType.FILE)
