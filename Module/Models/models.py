from typing import Any, Optional, Union, Callable
from datetime import datetime
from pydantic import BaseModel, Field
from settings import BPA_VERSION, BPA_NAME
from uuid import UUID


class PackageModel(BaseModel):
    uuid: str
    description: str
    date: Optional[str]
    date_of_actions: str
    destiny: Optional[str]
    actions: list[str]= []
    action_type: str
    package: Optional[dict[str, Any]]= {}
    
    class Config:
        json_schema_extra = {
            "description": "example_description",
            "date_of_actions": "13-02-2024 22:10:00",
            "destiny": "example_destiny",
            "actions": ["action1", "action2"],
            "action_type": "example_action_type",
            "package": {"key1": "value1"}
        }


class PackageInternalModel(PackageModel):
    processed: bool= False


class PackageScheduleModel(BaseModel):
    programmed_task: Any
    id_task: str
    date_object: datetime


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
