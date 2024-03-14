"""
- date: úselo cuando desee ejecutar el trabajo solo una vez en un momento determinado.
- inverval: utilícelo cuando desee ejecutar el trabajo en intervalos de tiempo fijos.
- cron: cuando desea ejecutar periódicamente el trabajo a determinadas horas del día.
"""
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Module.Models.models import PackageScheduleModel


scheduler = AsyncIOScheduler()

class ScheduleManagement:
    def __init__(self):
        self.active: bool= False
    
    async def config_start_or_shutdown_scheduler(self):
        """[config]: Inicia o apaga el schedule de acuerdo al valor de la variable de clase -active-."""
        if self.active:
            scheduler.start()
        else:
            scheduler.shutdown()
    
    async def change_scheduler_status(self, status: bool):
        """[method]: Inicia o apaga el schedule de acuerdo al boleano del parametro. -status- altera la variable de clase -active- para cambiar el estado de schedule."""
        self.active= status
        await self.config_start_or_shutdown_scheduler()
    
    async def schedule_set_date(self):
        """[advanced method]: Metodo que se encargara de crear la tarea segun el usuario."""
        pass
    
    async def schedule_add_job(self, package_schedule: PackageScheduleModel):
        """[method] Agrega el job (tarea) para que se ejecute en una fecha específica."""
        if self.active:
            scheduler.add_job(package_schedule.programmed_task, "date", run_date=package_schedule.date_object, id=package_schedule.id_task)
    
    async def remove_job_by_id(self, id_task: str):
        """[method]: Elimina el job (tarea) de acuerdo a su id (uuid del package) proporcionado."""
        if self.active:
            scheduler.remove_job(id_task)

#>> Instancia / objeto general de ScheduleManagement()
schedule_instance= ScheduleManagement()