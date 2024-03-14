import json
from fastapi import APIRouter, status
from Api.Config.methods import response_model_error
from Module.Core.Package.functions import PackageManagement
from Api.Services.ypw_account import UsersManagement
from Api.Schemas.schemas import PackageModel, TestScheduleModel
from Module.Models.models import PackageInternalModel


package_router= APIRouter(tags=["Package"])


pack_manage= PackageManagement()
user_account= UsersManagement()


async def get_all_sort():
    structured_packages= await pack_manage.sorting_package_by_date()
    print(structured_packages)


@package_router.post("/create")
async def register_package(package: PackageModel):
    """✅ Listo!"""
    if not await user_account.ypw_already_logged_in():
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "Necesita estar logueado.", None)
    
    date_object, formated_date, errors= await pack_manage.config_format_date_of_actions(package.date_of_actions)
    
    if errors["errors"]:
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "La fecha de acciones no tiene el formato esperado.", None)
    
    if not await pack_manage.compare_date_of_actions(date_object):
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "La fecha de acciones debe ser mayor a la fecha actual.", None)
    
    package_created = await pack_manage.create_new_package(
        package.description, formated_date, date_object, package.actions,
        package.action_type, package.package, package.destiny
    )
    #await pack_manage.processing_every_package()
    return response_model_error(status.HTTP_200_OK, False, "Package creado exitosamente.", package_created)


@package_router.delete("/delete")
async def delete_package(package: PackageInternalModel):
    
    if not await user_account.ypw_already_logged_in():
        return response_model_error(status.HTTP_400_BAD_REQUEST, True, "Necesita estar logueado.", None)
    
    package_data= PackageInternalModel(uuid=package.uuid, description=package.description, date=package.date, date_of_actions=package.date_of_actions, destiny=package.destiny, actions=package.actions, action_type=package.action_type, package=package.package, processed=package.processed)
    
    structured_packages, error= await pack_manage.remove_an_package(package_data)
    if error:
        return response_model_error(status.HTTP_404_NOT_FOUND, True, "Package no existente.", None)
    return response_model_error(status.HTTP_200_OK, False, "Package eliminado exitosamente.", structured_packages)

