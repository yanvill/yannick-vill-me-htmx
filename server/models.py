from enum import Enum

from pydantic import BaseModel


class FileNodeType(str, Enum):
    FILE = "FILE"
    DIR = "DIR"


class FileNode(BaseModel):
    path: str
    type: FileNodeType


class ListFilesResponse(BaseModel):
    files: list[FileNode]
