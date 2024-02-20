"""
functions.py se encargara de almacenar las funciones que tengas conexion directa con el package, por ejemplo, para crear un package, obtener, envio, eliminacion. CRUD de package.
"""
import uuid, json, os, time, pytz
from datetime import datetime
from settings import HASHING_UUID, PROJECT_NAME, BPA_VERSION, BPA_NAME, BPA_PATH
from Module.Models.models import PackageModel, PendingPackagesModel, BpaModel, ActionsType, PackageInternalModel
from Module.Core.Schedule.schedule_functions import ScheduleManagement


time_zone = pytz.timezone('America/Santo_Domingo')


class BpaManagement:
    def __init__(self):
        self.location_bpa= BPA_PATH
    
    async def config_exists_bpa(self):
        """[config]: Retorna True si el archivo bpa.json existe en el directorio, de lo contrario, retorna False."""
        return os.path.exists(self.location_bpa)
    
    async def config_counting_packages(self, data_packages: PendingPackagesModel):
        """[config]: Devuelve la cantidad de packages en BPA."""
        return len(data_packages.pending_packages)
    
    async def config_read_bpa(self):
        """[config]: Lee el BPA (Bank of pending actions) si existe o lo crea si es necesario."""
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
        """[method]: Agrega un nuevo package al pending_packages."""
        data_json = await self.config_read_bpa()
        data_json.pending_packages.append(dict(new_package))
        with open(self.location_bpa, 'w') as file:
            json.dump(dict(data_json), file, indent=4)
    
    async def remove_pending_packages(self, structured_packages: list, package: PackageInternalModel):
        """[method]: Elimina el package que se envie por parametro. \n- Retorna: tupla( structured_packages, error ) --> \n(list, False | list, True)"""
        try:
            structured_packages.remove(dict(package))
            print(dict(package), "no mames")
            return structured_packages, False
        except:
            print(dict(package), "klk")
            return structured_packages, True
    
    async def internal_structuring_pending_packages(self):
        """[config]: Pasa el bloque Pending packages (json) a formato de modelo para estructurarlo y poder manejarlo con facilidad. \n- Retorna: tupla[BpaModel, PendingPackagesModel]"""
        data_json= await self.config_read_bpa()
        structured_packages = PendingPackagesModel(pending_packages=[
            PackageInternalModel(**package_data) for package_data in data_json.pending_packages
        ])
        return data_json, structured_packages
    
    async def sorting_out_packages(self):
        """ LIFO (Last In First Out) """


class PackageManagement:
    def __init__(self):
        self.bpa_instance= BpaManagement()
        self.schedule_instance= ScheduleManagement()
        self.description: str
        self.date: datetime
        self.destiny: str
        self.actions: list
        self.action_type: str
        self.package: dict
        self.namespace_uuid= uuid.UUID(HASHING_UUID)
        self.format_date_of_actions: str= "%d-%m-%Y %H:%M:%S"
    
    async def config_exists_package(self, uuid: str):
        """[config]: Devuelve True si existe el package, de lo contrario False."""
        data_packages, structured_packages= await self.bpa_instance.internal_structuring_pending_packages()
        return any(package.uuid == uuid for package in structured_packages.pending_packages)
    
    async def compare_date_of_actions(self, date_of_actions: datetime):
        """[method]: Compara la fecha del package con la fecha actual para verificar que la fecha del package es mayor a la actual."""
        return time_zone.localize(date_of_actions) > datetime.now(time_zone)
    
    async def config_format_date_of_actions(self, date_of_actions: str):
        """[config]: Convierte la fecha de string -> datetime.
        \n=> tuple( str | none, false | true )."""
        errors= {"errors": False}
        try:
            date_object= datetime.strptime(date_of_actions, self.format_date_of_actions)
            return date_object, date_object.strftime(self.format_date_of_actions), errors
        except ValueError:
            errors["errors"]= True
            return None, None, errors
    
    
    async def processing_every_package(self):
        """[method]: Metodo principal para procesar cada package pendiente en el BPA (Bank of Pending Actions)."""
        data_packages, structured_packages = await self.bpa_instance.internal_structuring_pending_packages()
        
        for package in structured_packages.pending_packages:
            date_object, formated_date, errors= await self.config_format_date_of_actions(package.date_of_actions)
            
            #>> si la fecha del package es menor entonces ya el package fue procesado, y devuelve False, por lo que no entra al bloque.
            if self.compare_date_of_actions(date_object):
                #>> si el package no se ha procesado entonces se inicia su procesamiento, valga la redundancia.
                await self.processing_package(package)
            
            #>> como el package fue procesado entonces se actualiza a True.
            package.processed= True
            if package.processed:
                await self.schedule_instance.remove_job_by_id(package.uuid) #>> se elimina la tarea del scheduler.
                data_packages.pending_packages, error= await self.bpa_instance.remove_pending_packages(data_packages.pending_packages, package) #>> se elimina el package del BPA.
                
                with open(BPA_PATH, 'w') as file:
                    json.dump(dict(data_packages), file, indent=4)
    
    async def processing_package(self, package: PackageInternalModel):
        """[method]: Para procesar el package pendiente en turno."""
        pass
    
    async def create_new_package(self, description: str, date_of_actions: str, actions: list, action_type: str, package: dict, destiny: str="./"):
        """[method]: Crea un nuevo package, luego lo inserta directamente en el BPA (Bank of Pending Actions)."""
        date=datetime.now(time_zone).strftime(self.format_date_of_actions)
        new_package= PackageInternalModel(
            uuid=str(uuid.uuid5(self.namespace_uuid, f"{PROJECT_NAME}{date}")),
            description=description, date=date, date_of_actions=date_of_actions,
            destiny="./", actions=actions, action_type=action_type,
            package=package
        )
        await self.bpa_instance.update_pending_packages(new_package)
        return new_package
    
    async def get_packages(self):
        """[method]: Obtiene una lista de los packages del BPA (Bank of Pending Actions)."""
        bpa_json, structured_packages= await self.bpa_instance.internal_structuring_pending_packages()
        return structured_packages.pending_packages
    
    async def remove_an_package(self, package: PackageInternalModel):
        """[method]: Elimina el package que se envie por parametro."""
        bpa_json, structured_packages= await self.bpa_instance.internal_structuring_pending_packages()
        
        structured_packages.pending_packages, error = await self.bpa_instance.remove_pending_packages(structured_packages.pending_packages, package)
        return structured_packages.pending_packages, error
    
    async def sorting_package_by_date(self):
        """[method]: Ordena / sortea los packages de forma ascendente (FIFO: First In, First Out)."""
        bpa_json, structured_packages = await self.bpa_instance.internal_structuring_pending_packages()
        structured_packages.pending_packages.sort(key=lambda x: x.date)
        return structured_packages


class DatabaseManagement:
    def __init__(self):
        self.type_db= "MySQL"

