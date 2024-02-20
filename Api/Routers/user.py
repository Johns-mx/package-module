import json
from fastapi import APIRouter, status
from Api.Config.methods import response_model_error
from Module.Core.Package.functions import PackageManagement
from Api.Schemas.schemas import UserSettingsModel, YpwDataOne, YpwDataThree, YpwDataTwo, YpwDeveloperModel, YpwLogin, YpwLoginInternal, YpwMainModel, YpwModel, YpwRequestUsers, RequestType
from Api.Services.ypw_account import YpwAccountManagement, UsersManagement
from settings import YPW_PRIVATE_KEY, YPW_PUBLIC_KEY, YPW_APP_CONNECT


user_router= APIRouter(tags=["Users"])


request= YpwRequestUsers()
request_type= RequestType()


@user_router.post("/login")
async def login_user(user: YpwLogin):
    """✅ Listo!"""
    ypw_account= YpwAccountManagement()
    user_account= UsersManagement()
    
    user_data, status_response= await ypw_account.ypw_request_user(request_type.POST, request.login, YpwLoginInternal(username=user.username, password=user.password))
    
    if user_data is None:
        return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
    if user_data.error:
        return response_model_error(status_response, True, user_data.message, None)
    
    #>> Se deben guardar los datos del usuario al archivo settings.json que correponde al almacenamiento de datos del usaurio.
    data= UserSettingsModel(keyUser=user_data.res["keyUser"])
    await user_account.update_settings_json(data)
    return response_model_error(status.HTTP_200_OK, False, "Usuario logueado exitosamente.", None)

