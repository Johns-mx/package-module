"""
functions.py se encargara de almacenar las funciones que tengas conexion directa con el package, por ejemplo, para crear un package, obtener, envio, eliminacion. CRUD de package.
"""
import uuid, json, os
from datetime import datetime
from settings import HASHING_UUID, PROJECT_NAME, BPA_VERSION, BPA_NAME
from Module.Models.models import PackageModel, PendingPackagesModel, BpaModel, ActionsType, PackageInternalModel


class BpaManagement:
    def __init__(self):
        self.location_bpa= "Module/Core/Package/bpa.json"
    
    async def config_exists_bpa(self):
        return os.path.exists(self.location_bpa)
    
    async def config_read_bpa(self):
        bpa_content = {
            "project": BPA_NAME,
            "version": BPA_VERSION,
            "pending_packages": []
        }
        if not await self.config_exists_bpa():
            with open(self.location_bpa, 'w') as file:
                json.dump(bpa_content, file, indent=4)
            return BpaModel(**bpa_content)
        
        #>> El archivo existe, verificamos si está vacío
        if os.path.getsize(self.location_bpa) == 0:
            with open(self.location_bpa, 'w') as file:
                json.dump(bpa_content, file, indent=4)
            return BpaModel(**bpa_content)
        
        with open(self.location_bpa, 'r') as file:
            bpa_dict = json.load(file)
        return BpaModel(**bpa_dict)
    
    async def update_pending_packages(self, new_package: PackageModel):
        data_json = await self.config_read_bpa()
        data_json.pending_packages.append(dict(new_package))
        with open(self.location_bpa, 'w') as file:
            json.dump(dict(data_json), file, indent=4)
    
    async def remove_pending_packages(self, package):
        data_json = await self.config_read_bpa()
        data_json.pending_packages.remove(package)
        with open(self.location_bpa, 'w') as file:
            json.dump(data_json, file, indent=4)
    
    async def internal_structuring_pending_packages(self):
        data_json= await self.config_read_bpa()
        uuids_packages: list= []
        data_packages = PendingPackagesModel(pending_packages=[
            PackageInternalModel(**package_data) for package_data in data_json.pending_packages
        ])
        for package in data_packages.pending_packages:
            uuids_packages.append(package.uuid)
            uuids_packages.append(package.processed)
            uuids_packages.append(datetime.strptime(package.date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S.%f"))
        return uuids_packages
    
    async def sorting_out_packages(self):
        """ LIFO (Last In First Out) """
        data_json= await self.config_read_bpa()


class PackageManagement:
    def __init__(self):
        self.description: str
        self.date: datetime
        self.destiny: str
        self.actions: list
        self.action_type: str
        self.package: dict
        self.namespace_uuid= uuid.UUID(HASHING_UUID)
    
    async def config_exists_package(self):
        pass
    
    async def create_new_package(self, description: str, actions: list, action_type: str, package: dict, destiny: str="./"):
        date=datetime.now()
        new_package= PackageInternalModel(
            uuid=str(uuid.uuid5(self.namespace_uuid, f"{PROJECT_NAME}{date}")),
            description=description, date=date.isoformat(),
            destiny="./", actions=actions, action_type=action_type,
            package=package
        )
        bpa_instance= BpaManagement()
        await bpa_instance.update_pending_packages(new_package)
        return new_package
    
    async def get_package(self):
        bpa_instance= BpaManagement()
        return await bpa_instance.internal_structuring_pending_packages()
    
    async def remove_package(self):
        pass
    
    async def sorting_package(self):
        pass


class DatabaseManagement:
    def __init__(self):
        self.type_db= "MySQL"
