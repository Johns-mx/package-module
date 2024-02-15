import requests, json
from fastapi import status
from settings import PROJECT_NAME, YPW_URL, YPW_PUBLIC_KEY, YPW_PRIVATE_KEY
from Api.Schemas.schemas import YpwLogin, YpwLoginInternal, YpwMainModel, RequestType, YpwRequestUsers, YpwResponseModel, YpwDeveloperModel, YpwDataOne, YpwKeys, YpwDataTwo
from Api.Config.methods import response_model_error


request= YpwRequestUsers()
request_type= RequestType()


class YpwAccountManagement:
    def __init__(self):
        self.BASE_URL: str= YPW_URL
    
    async def config_processing_data_request(self, user_data: YpwResponseModel):
        if user_data is None:
            return None
        if user_data.error:
            return user_data.message
        return user_data.res
    
    async def ypw_request_user(self, request_type: str, url_request: str, data: YpwMainModel | YpwLoginInternal):
        """Get user / Login / Logout: (appConnect, keyUser)"""
        try:
            payload= json.dumps(dict(data))
            headers= {'Content-Type': 'application/json'}
            response= requests.request(request_type, f"{self.BASE_URL}{url_request}", headers=headers, data=payload)
            
            return YpwResponseModel(**json.loads(response.text)), response.status_code
        except requests.exceptions.RequestException:
            return None, None
    
    async def ypw_request_data(self, request_type: str, url_request: str, payload: YpwDeveloperModel | YpwDataOne | YpwDataTwo):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.request(request_type, f"{self.BASE_URL}{url_request}", headers=headers, data=json.dumps(dict(payload)))
            
            return YpwResponseModel(**json.loads(response.text)), response.status_code
        except requests.exceptions.RequestException:
            return None, None


class UsersManagement:
    def __init__(self):
        self.ypw_account= YpwAccountManagement()