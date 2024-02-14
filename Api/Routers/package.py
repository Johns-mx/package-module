from fastapi import APIRouter, status
from Api.Config.methods import response_model_error, version
from Module.Core.Package.functions import PackageManagement
from Api.Schemas.schemas import PackageModel


package_router= APIRouter(prefix=f"/api/v{version.major}/package")


@package_router.get("/get")
async def get_package():
    #>> codigo solo de prueba
    pack_manage= PackageManagement()
    await pack_manage.processing_packages()


@package_router.get("/get_all")
async def get_all_package():
    #>> codigo solo de prueba
    pack_manage= PackageManagement()
    return await pack_manage.get_package()


@package_router.post("/create")
async def register_package(package: PackageModel):
    pack_manage= PackageManagement()    
    date_object, formated_date, errors= await pack_manage.config_format_date_of_actions(package.date_of_actions)
    
    if errors["errors"]:
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "La fecha de acciones no tiene el formato esperado.", None)
    
    if not await pack_manage.compare_date_of_actions(date_object):
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "La fecha de acciones debe ser mayor a la fecha actual.", None)
    
    package_created = await pack_manage.create_new_package(
        package.description, formated_date, package.actions,
        package.action_type, package.package, package.destiny
    )
    return response_model_error(status.HTTP_200_OK, False, "Package creado exitosamente.", package_created)


@package_router.delete("/delete")
async def delete_package():
    pass