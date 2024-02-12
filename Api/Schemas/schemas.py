from pydantic import BaseModel
from typing import Optional, Any


class VersionProject(BaseModel):
    ver: str= ""
    major: int
    minor: int
    patch: int


class PackageModel(BaseModel):
    description: str
    actions: list[str]= []
    action_type: str
    package: Optional[dict[str, Any]]= {}
    destiny: Optional[str]= ""