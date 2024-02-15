from pydantic import BaseModel
from typing import Optional, Any, Union
from datetime import datetime
from settings import PROJECT_NAME, YPW_APP_CONNECT, YPW_PUBLIC_KEY, YPW_PRIVATE_KEY


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


class YpwResponseModel(BaseModel):
    error: bool
    message: str
    res: Any
    version: str


class YpwRequestUsers(BaseModel):
    getUser: str= "/account/getUser"
    registrar: str= "/account/register"
    login: str= "/account/login"
    logout: str= "/account/logout"
    data_get: str= "/account/data/get"
    data_isKey: str= "/account/data/isKey"
    data_keys: str= "/account/data/keys"
    data_create: str= "/account/data/create"
    data_set: str= "/account/data/set"
    data_remove: str= "/account/data/remove"

class YpwMainModel(BaseModel):
    appConnect: str
    keyUser: str


class YpwDeveloperModel(BaseModel):
    public_key: Optional[str]= YPW_PUBLIC_KEY
    private_key: Optional[str]= YPW_PRIVATE_KEY


class YpwDataOne(YpwDeveloperModel):
    keyData: str


class YpwDataTwo(YpwDeveloperModel):
    keyData: str
    Data: str

class YpwLogin(BaseModel):
    username: str
    password: str

class YpwLoginInternal(YpwLogin):
    appConnect: Optional[str]= YPW_APP_CONNECT

class RequestType(BaseModel):
    GET: str= "GET"
    POST: str= "POST"
    DELETE: str= "DELETE"
    PUT: str= "PUT"

class YpwKeys:
    id: Optional[int]
    public: str
    private: str

class YpwLoginKeys(BaseModel):
    appConnect: Optional[str]= ""
    keyUser: Optional[str]= ""
