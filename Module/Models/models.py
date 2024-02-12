from typing import Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from settings import BPA_VERSION, BPA_NAME


class PackageModel(BaseModel):
    uuid: str
    description: str
    date: datetime
    destiny: Optional[str]
    actions: list[str]= []
    action_type: str
    package: Optional[dict[str, Any]]= {}


class BpaStoreModel(BaseModel):
    BPA: Optional[dict[str, Any]] = None


class PendingPackagesModel(BaseModel):
    pending_packages: Optional[list]= []


class BpaModel(BaseModel):
    project: str= BPA_NAME
    version: str= BPA_VERSION
    pending_packages: list= []