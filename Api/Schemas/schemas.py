from pydantic import BaseModel
from typing import Optional, Any, Union
from datetime import datetime


class VersionProject(BaseModel):
    ver: str= ""
    major: int
    minor: int
    patch: int


class PackageModel(BaseModel):
    description: str
    date_of_actions: str
    actions: list[str]= []
    action_type: str
    package: Optional[dict[str, Any]]= {}
    destiny: Optional[str]= ""