import os
import requests, json
from fastapi import status
from settings import PROJECT_NAME, YPW_URL, YPW_PUBLIC_KEY, YPW_PRIVATE_KEY
from Api.Schemas.schemas import UserSettingsModel, YpwDataThree, YpwLogin, YpwLoginInternal, YpwMainModel, RequestType, YpwModel, YpwRequestUsers, YpwResponseModel, YpwDeveloperModel, YpwDataOne, YpwKeys, YpwDataTwo
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
    
    async def ypw_request_data(self, request_type: str, url_request: str, payload: YpwDeveloperModel | YpwDataOne | YpwDataTwo | YpwDataThree):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.request(request_type, f"{self.BASE_URL}{url_request}", headers=headers, data=json.dumps(dict(payload)))
            
            return YpwResponseModel(**json.loads(response.text)), response.status_code
        except requests.exceptions.RequestException:
            return None, None


class UsersManagement:
    def __init__(self):
        self.ypw_account= YpwAccountManagement()
        self.location_settings= "/PackageModule/settings.json"
    
    async def config_read_settings(self):
        """[config]: Lee el archivo settings.json si existe, o lo crea si es necesario."""
        settings_content = {
            "keyUser": "",
            "appConnect": "",
            "data": []
        }
        if not os.path.exists(self.location_settings):
            with open(self.location_settings, 'w') as file:
                json.dump(settings_content, file, indent=4)
            return UserSettingsModel(**settings_content)
        
        #>> El archivo existe, verificamos si está vacío
        if os.path.getsize(self.location_settings) == 0:
            with open(self.location_settings, 'w') as file:
                json.dump(settings_content, file, indent=4)
            return UserSettingsModel(**settings_content)
        
        with open(self.location_settings, 'r') as file:
            settings_dict = json.load(file)
        return UserSettingsModel(**settings_dict)
    
    async def update_settings_json(self, data: UserSettingsModel):
        """[method]: Actualizar settings.json"""
        data_json = await self.config_read_settings()
        data_json.keyUser= data.keyUser
        data_json.appConnect= data.appConnect
        with open(self.location_settings, 'w') as file:
            json.dump(dict(data_json), file, indent=4)
    
    
    async def config_ypw_response(self, response: YpwResponseModel):
        if response is None or response.error:
            return None
        return response.res
    
    
    async def ypw_get_user(self):
        """✅ Listo!"""
        data_user= await self.config_read_settings()
        user_data, status_response= await self.ypw_account.ypw_request_user(request_type.POST, request.getUser, YpwMainModel(appConnect=data_user.appConnect, keyUser=data_user.keyUser))
        
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, None)
        return response_model_error(status.HTTP_200_OK, False, "Usuario obtenido exitosamente.", user_data.res)
    
    
    async def ypw_logout_user(self):
        """✅ Listo!"""
        data_user= await self.config_read_settings()
        user_data, status_response= await self.ypw_account.ypw_request_user(request_type.POST, request.logout, YpwMainModel(keyUser=data_user.keyUser, appConnect=data_user.appConnect))
        
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, None)
        return response_model_error(status.HTTP_200_OK, False, "Session eliminada exitosamente.", None)
    
    async def ypw_get_data(self, data: YpwDataOne):
        """✅ Listo!"""
        user_data, status_response= await self.ypw_account.ypw_request_data(request_type.POST, request.data_get, data)
        
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, user_data.res)
        return response_model_error(status.HTTP_200_OK, False, "Data obtenida exitosamente.", user_data.res)
    
    async def ypw_create_data(self, user_keys: YpwDeveloperModel):
        """✅ Listo!"""
        klk={"shop_data": "no mames"}
        
        payload= YpwDataTwo(public_key=user_keys.public_key, private_key=user_keys.private_key, keyData="YPW_APP_CONNECT", Data=json.dumps(klk))
        
        if not payload.keyData or not payload.Data:
            return response_model_error(status.HTTP_400_BAD_REQUEST, True, "Los campos 'keyData' y 'Data' son obligatorios.", None)
        
        user_data, status_response= await self.ypw_account.ypw_request_data(request_type.POST, request.data_create, payload=payload)
        
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, None)
        
        return response_model_error(status.HTTP_200_OK, False, "Data creada exitosamente.", user_data.res)
    
    async def keys_data(self, user: YpwDeveloperModel):
        """✅ Listo!"""
        user_data, status_response= await self.ypw_account.ypw_request_data(request_type.POST, request.data_keys, user)
        
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, None)
        
        return response_model_error(status.HTTP_200_OK, False, "Data creada exitosamente.", user_data.res)
    
    async def update_data(self, user_keys: YpwDeveloperModel):
        """✅ Listo!"""
        klk={"shop_data": "no mames"}
        
        payload= YpwDataTwo(public_key=user_keys.public_key, private_key=user_keys.private_key, keyData="package-module-app", Data=json.dumps(klk))
        
        user_data, status_response= await self.ypw_account.ypw_request_data(request_type.PUT, request.data_set, payload=payload)
        
        if not payload.keyData or not payload.Data:
            return response_model_error(status.HTTP_400_BAD_REQUEST, True, "Los campos 'keyData' y 'Data' son obligatorios.", None)
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, None)
        
        return response_model_error(status.HTTP_200_OK, False, "Data actualizada exitosamente.", user_data.res)
    
    async def delete_data(self, user_keys: YpwDataOne):
        """✅ Listo!"""
        if not user_keys.keyData:
            return response_model_error(status.HTTP_400_BAD_REQUEST, True, "El campo 'Data' es obligatorio.", None)
        
        user_data, status_response= await self.ypw_account.ypw_request_data(request_type.DELETE, request.data_remove, payload=user_keys)
        
        if user_data is None:
            return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
        if user_data.error:
            return response_model_error(status_response, True, user_data.message, None)
        
        return response_model_error(status.HTTP_200_OK, False, "Data eliminada exitosamente.", user_data.res)


class DataManagement:
    def __init__(self):
        self.type_db= "MySQL"
    
    async def get_data(self):
        pass
    
    async def create_data(self):
        pass
    
    async def update_data(self):
        pass
    
    async def delete_data(self):
        pass