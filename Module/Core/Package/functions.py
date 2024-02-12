"""
functions.py se encargara de almacenar las funciones que tengas conexion directa con el package, por ejemplo, para crear un package, obtener, envio, eliminacion. CRUD de package.
"""
import uuid, json, os
from datetime import datetime
from settings import HASHING_UUID, PROJECT_NAME, BPA_VERSION, BPA_NAME
from Models.models import PackageModel, PendingPackagesModel, BpaModel



class BpaManagement:
    def __init__(self):
        self.location_bpa= "./bpa.json"
    
    def config_exists_bpa(self):
        return os.path.exists(self.location_bpa)
    
    def config_read_bpa(self):
        if not self.config_exists_bpa():
            bpa_json = BpaModel()
            with open(self.location_bpa, 'w') as file:
                json.dump(bpa_json, file, indent=4)
            return bpa_json
        
        with open(self.location_bpa, 'r+') as file:
            bpa_json= file.read()
            bpa_json: BpaModel = json.loads(bpa_json)
            return bpa_json
    
    def update_pending_packages(self, new_package: PackageModel):
        data_json = self.config_read_bpa()
        data_json.pending_packages.append(new_package)
        with open(self.location_bpa, 'w') as file:
            json.dump(data_json, file, indent=4)
    
    def remove_pending_packages(self, package):
        data_json = self.config_read_bpa()
        data_json.pending_packages.remove(package)
        with open(self.location_bpa, 'w') as file:
            json.dump(data_json, file, indent=4)
    
    def sorting_out_packages(self):
        pass


class PackageManagement:
    def __init__(self):
        self.description: str
        self.date: datetime
        self.destiny: str
        self.actions: list
        self.action_type: str
        self.package: dict
    
    def config_exists_package(self):
        pass
    
    def create_new_package(self, description: str, actions: list, action_type: str, package: dict, destiny: str=None):
        date=datetime.now()
        new_package= PackageModel(
            uuid=uuid.uuid5(uuid.UUID(HASHING_UUID), f"{PROJECT_NAME}{date}"),
            description=description, date=date,
            destiny="./", actions=actions, action_type=action_type,
            package=package
        )
        bpa_instance= BpaManagement()
        bpa_instance.update_pending_packages(new_package)
    
    def get_package(self, ):
        pass
    
    def remove_package(self):
        pass
    
    def sorting_package(self):
        pass


class DatabaseManagement:
    def __init__(self):
        self.type_db= "MySQL"
