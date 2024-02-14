"""
functions.py se encargara de almacenar las funciones que tengas conexion directa con el package, por ejemplo, para crear un package, obtener, envio, eliminacion. CRUD de package.
"""
import uuid, json, os, time, pytz
from datetime import datetime
from settings import HASHING_UUID, PROJECT_NAME, BPA_VERSION, BPA_NAME
from Module.Models.models import PackageModel, PendingPackagesModel, BpaModel, ActionsType, PackageInternalModel


time_zone = pytz.timezone('America/Santo_Domingo')


class BpaManagement:
    def __init__(self):
        self.location_bpa= "Module/Core/Package/bpa.json"
    
    async def config_exists_bpa(self):
        return os.path.exists(self.location_bpa)
    
    async def config_counting_packages(self, data_packages: PendingPackagesModel):
        return len(data_packages.pending_packages)
    
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
    
    async def remove_pending_packages(self, structured_packages: list, package: PackageInternalModel):
        structured_packages.remove(dict(package))
        return structured_packages
    
    async def internal_structuring_pending_packages(self):
        data_json= await self.config_read_bpa()
        structured_packages = PendingPackagesModel(pending_packages=[
            PackageInternalModel(**package_data) for package_data in data_json.pending_packages
        ])
        return data_json, structured_packages
    
    async def processing_every_package(self):
        data_packages, structured_packages = await self.internal_structuring_pending_packages()
        
        for package in structured_packages.pending_packages:
            if package.processed == True:
                time.sleep(2)
                data_packages.pending_packages= await self.remove_pending_packages(data_packages.pending_packages, package)
                
                with open(self.location_bpa, 'w') as file:
                    json.dump(dict(data_packages), file, indent=4)
    
    async def sorting_out_packages(self):
        """ LIFO (Last In First Out) """


class PackageManagement:
    def __init__(self):
        self.bpa_instance= BpaManagement()
        self.description: str
        self.date: datetime
        self.destiny: str
        self.actions: list
        self.action_type: str
        self.package: dict
        self.namespace_uuid= uuid.UUID(HASHING_UUID)
        self.format_date_of_actions: str= "%d-%m-%Y %H:%M:%S"
    
    async def config_exists_package(self, uuid: str):
        data_packages, structured_packages= await self.bpa_instance.internal_structuring_pending_packages()
        return any(package.uuid == uuid for package in structured_packages.pending_packages)
    
    async def compare_date_of_actions(self, date_of_actions: datetime):
        return time_zone.localize(date_of_actions) > datetime.now(time_zone)
    
    async def config_format_date_of_actions(self, date_of_actions: str):
        """Convierte la fecha de string -> datetime.
        \n=> tuple( str | none, false | true )."""
        errors= {"errors": False}
        try:
            date_object= datetime.strptime(date_of_actions, self.format_date_of_actions)
            return date_object, date_object.strftime(self.format_date_of_actions), errors
        except ValueError:
            errors["errors"]= True
            return None, None, errors
    
    async def processing_packages(self):
        await self.bpa_instance.processing_every_package()
    
    async def create_new_package(self, description: str, date_of_actions: str, actions: list, action_type: str, package: dict, destiny: str="./"):
        date=datetime.now(time_zone)
        new_package= PackageInternalModel(
            uuid=str(uuid.uuid5(self.namespace_uuid, f"{PROJECT_NAME}{date}")),
            description=description, date=date.isoformat(), date_of_actions=date_of_actions,
            destiny="./", actions=actions, action_type=action_type,
            package=package
        )
        await self.bpa_instance.update_pending_packages(new_package)
        return new_package
    
    async def get_package(self):
        return await self.bpa_instance.internal_structuring_pending_packages()
    
    async def remove_package(self):
        pass
    
    async def sorting_package(self):
        pass


class DatabaseManagement:
    def __init__(self):
        self.type_db= "MySQL"





"SELECT * FROM db.students where users.edad == 18"


