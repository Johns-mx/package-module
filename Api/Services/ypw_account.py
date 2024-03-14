import requests, json, os
from fastapi import status
from Module.Core.Package.functions import BpaManagement
from Module.Core.Schedule.schedule_functions import schedule_instance
from settings import BPA_PATH, PROJECT_NAME, YPW_URL, YPW_PUBLIC_KEY, YPW_PRIVATE_KEY, SETTINGS_PATH
from Api.Schemas.schemas import UserSettingsModel, YpwDataMain, YpwDataThree, YpwLogin, YpwLoginInternal, YpwMainModel, RequestType, YpwModel, YpwRequestUsers, YpwResponseModel, YpwDeveloperModel, YpwDataOne, YpwKeys, YpwDataTwo


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
        self.bpa_instance= BpaManagement()
        self.location_settings: str= SETTINGS_PATH
    
    async def startup_all_internal_process(self):
        """[config | method (ENCIENDE)]: Crea los archivos settings y bpa. Inicia los procesos de apscheduler."""
        await schedule_instance.change_scheduler_status(True)
        bpa= await self.bpa_instance.config_read_bpa()
    

    async def shutdown_all_internal_process(self):
        """[config | method (APAGAR)]: Elimina los archivos settings y bpa. Cancela los procesos de apscheduler."""
        await schedule_instance.change_scheduler_status(False)
        os.remove(self.location_settings)
        os.remove(BPA_PATH)
    

    async def ypw_already_logged_in(self):
        """[method]: Retorna True si el usuario ya esta logueado, de lo contrario, False."""
        data_response, status_response= await self.ypw_get_user()
        if status_response not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            return False
        return True
    

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
    
    
    async def config_ypw_process_response(self, response: YpwResponseModel, status_code):
        if response is None or response.error or status_code not in (status.HTTP_200_OK, status.HTTP_201_CREATED):
            return None, None
        return response.res, response.error
    

    async def ypw_get_user(self):
        """✅ Listo! [method]: Obtiene la session del usuario guardada en settings.json y realizar una peticion a db para obtener los datos del usuario."""
        data_settings= await self.config_read_settings()
        data_response, status_response= await self.ypw_account.ypw_request_user(request_type.POST, request.getUser, YpwMainModel(appConnect=data_settings.appConnect, keyUser=data_settings.keyUser))
        return data_response, status_response
    

    async def ypw_logout_user(self):
        """✅ Listo! [method]: Obtiene la session del usuario guardada en settings.json, para proceder a cerrar la session guardada."""
        data_settings= await self.config_read_settings()
        data_response, status_response= await self.ypw_account.ypw_request_user(request_type.POST, request.logout, YpwMainModel(keyUser=data_settings.keyUser, appConnect=data_settings.appConnect))
        return data_response, status_response
    

    async def ypw_get_data(self, data: YpwDataOne):
        """✅ Listo!"""
        data_response, status_response= await self.ypw_account.ypw_request_data(request_type.POST, request.data_get, data)
        return data_response, status_response
    

    async def ypw_create_data(self, payload: YpwDataTwo):
        """✅ Listo!"""
        data_response, status_response= await self.ypw_account.ypw_request_data(request_type.POST, request.data_create, payload=json.dumps(payload))
        return data_response, status_response
    

    async def ypw_keys_data(self, user: YpwDeveloperModel):
        """✅ Listo!"""
        data_response, status_response= await self.ypw_account.ypw_request_data(request_type.POST, request.data_keys, user)
        return data_response, status_response
    

    async def ypw_update_data(self, payload: YpwDataTwo):
        """✅ Listo!"""
        #if not payload.keyData or not payload.Data:
            #return response_model_error(status.HTTP_400_BAD_REQUEST, True, "Los campos 'keyData' y 'Data' son obligatorios.", None)
        data_response, status_response= await self.ypw_account.ypw_request_data(request_type.PUT, request.data_set, payload=json.dumps(payload))
        return data_response, status_response
    
    
    async def ypw_delete_data(self, user_keys: YpwDataOne):
        """✅ Listo!"""
        #if not user_keys.keyData:
            #return response_model_error(status.HTTP_400_BAD_REQUEST, True, "El campo 'Data' es obligatorio.", None)
        data_response, status_response= await self.ypw_account.ypw_request_data(request_type.DELETE, request.data_remove, payload=user_keys)
        return data_response, status_response


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