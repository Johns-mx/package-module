from fastapi import APIRouter, status
from Api.Config.methods import response_model_error, version
from Module.Core.Package.functions import PackageManagement
from Api.Schemas.schemas import YpwLogin, YpwLoginInternal, YpwRequestUsers, RequestType
from Api.Services.ypw_account import YpwAccountManagement
from settings import YPW_PRIVATE_KEY, YPW_PUBLIC_KEY


user_router= APIRouter(prefix=f"/api/v{version.major}/user", tags=["Users"])


request= YpwRequestUsers()
request_type= RequestType()


@user_router.post("/login")
async def login_user(user: YpwLogin):
    ypw_account= YpwAccountManagement()
    user_data, status_response= await ypw_account.ypw_request_user(request_type.POST, request.login, YpwLoginInternal(username=user.username, password=user.password))
    
    if user_data is None:
        return response_model_error(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al procesar la peticion.", None)
    
    if user_data.error:
        return response_model_error(status_response, True, user_data.message, None)
    
    return response_model_error(status.HTTP_200_OK, False, "Usuario logueado exitosamente.", user_data.res)

