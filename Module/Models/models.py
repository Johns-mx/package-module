from typing import Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from settings import BPA_VERSION, BPA_NAME
from uuid import UUID


class PackageModel(BaseModel):
    uuid: str
    description: str
    date: Union[datetime, str]
    destiny: Optional[str]
    actions: list[str]= []
    action_type: str
    package: Optional[dict[str, Any]]= {}


class PackageInternalModel(PackageModel):
    processed: bool= False


class PendingPackagesModel(BaseModel):
    pending_packages: Optional[list[PackageInternalModel]]


class BpaStoreModel(BaseModel):
    BPA: Optional[dict[str, Any]] = None


class BpaModel(BaseModel):
    project: str= BPA_NAME
    version: str= BPA_VERSION
    pending_packages: list= []


class ActionsType(BaseModel):
    GET: str= "GET"
    POST: str= "POST"
    DELETE: str= "DELETE"
    UPDATE: str= "UPDATE"
