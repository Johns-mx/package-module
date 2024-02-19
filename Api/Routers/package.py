import json
from fastapi import APIRouter, status
from Api.Config.methods import response_model_error
from Module.Core.Package.functions import PackageManagement
from Api.Schemas.schemas import PackageModel
from Module.Models.models import PackageInternalModel


package_router= APIRouter(tags=["Package"])


@package_router.get("/get")
async def get_package():
    #>> codigo solo de prueba
    pack_manage= PackageManagement()
    await pack_manage.processing_packages()


@package_router.get("/get_all_sort")
async def get_all_sort():
    pack_manage= PackageManagement()
    structured_packages= await pack_manage.sorting_package_by_date()
    return structured_packages


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
async def delete_package(package: PackageInternalModel):
    
    package_data= PackageInternalModel(uuid=package.uuid, description=package.description, date=package.date, date_of_actions=package.date_of_actions, destiny=package.destiny, actions=package.actions, action_type=package.action_type, package=package.package, processed=package.processed)
    pack_manage= PackageManagement()
    structured_packages, error= await pack_manage.remove_an_package(package_data)
    if error:
        return response_model_error(status.HTTP_404_NOT_FOUND, True, "Package no existente.", None)
    return response_model_error(status.HTTP_200_OK, False, "Package eliminado exitosamente.", structured_packages)

