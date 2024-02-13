from fastapi import APIRouter
from Api.Config.methods import version
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
    package_created = await pack_manage.create_new_package(
        package.description, package.actions,
        package.action_type, package.package,
        package.destiny
    )
    return package_created


@package_router.delete("/delete")
async def delete_package():
    pass