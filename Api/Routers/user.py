import json, os
from fastapi import APIRouter, status
from Api.Config.methods import response_model_error
from Module.Core.Package.functions import PackageManagement
from Module.Core.Schedule.schedule_functions import ScheduleManagement
from Api.Schemas.schemas import UserSettingsModel, YpwDataOne, YpwDataThree, YpwDataTwo, YpwDeveloperModel, YpwLogin, YpwLoginInternal, YpwMainModel, YpwModel, YpwRequestUsers, RequestType
from Api.Services.ypw_account import YpwAccountManagement, UsersManagement
from settings import SETTINGS_PATH


user_router= APIRouter(tags=["Users"])


request= YpwRequestUsers()
request_type= RequestType()

ypw_account= YpwAccountManagement()
user_account= UsersManagement()
schedule_instance= ScheduleManagement()


@user_router.post("/login")
async def login_user(user: YpwLogin):
    """✅ Listo!"""    
    if await user_account.ypw_already_logged_in():
        return response_model_error(status.HTTP_409_CONFLICT, True, "El usuario ya esta logueado.", None)
    
    user_data, status_response= await ypw_account.ypw_request_user(request_type.POST, request.login, YpwLoginInternal(username=user.username, password=user.password))
    
    if user_data is None:
        return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
    if user_data.error:
        return response_model_error(status_response, True, user_data.message, None)
    
    #>> Se deben guardar los datos del usuario al archivo settings.json que correponde al almacenamiento de datos del usaurio.
    data= UserSettingsModel(keyUser=user_data.res["keyUser"])
    await user_account.update_settings_json(data)
    
    await user_account.startup_all_internal_process()
    return response_model_error(status.HTTP_200_OK, False, "Usuario logueado exitosamente.", None)


@user_router.get("/logout")
async def logout_user():
    """✅ Listo!"""
    if not await user_account.ypw_already_logged_in():
        os.remove(SETTINGS_PATH)
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "Necesita estar logueado.", None)
    
    user_data, status_response= await user_account.ypw_logout_user()
    if user_data is None:
        return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
    
    if user_data.error:
        return response_model_error(status_response, True, user_data.message, None)
    
    #>> Se deben guardar los datos del usuario al archivo settings.json que correponde al almacenamiento de datos del usaurio.
    data= YpwMainModel()
    await user_account.update_settings_json(data)
    await user_account.shutdown_all_internal_process()
    return response_model_error(status.HTTP_200_OK, False, "Session cerrada exitosamente.", None)
