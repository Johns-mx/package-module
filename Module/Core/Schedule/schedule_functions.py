"""
- date: úselo cuando desee ejecutar el trabajo solo una vez en un momento determinado.
- inverval: utilícelo cuando desee ejecutar el trabajo en intervalos de tiempo fijos.
- cron: cuando desea ejecutar periódicamente el trabajo a determinadas horas del día.
"""
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


class ScheduleManagement:
    def __init__(self):
        self.active: bool= False
    
    async def config_start_or_shutdown_scheduler(self):
        if self.active:
            await scheduler.start()
        else:
            await scheduler.shutdown()
    
    async def change_scheduler_status(self, status: bool):
        self.active= status
        await self.config_start_or_shutdown_scheduler()
    
    async def set_date(self):
        """[advanced method]: Metodo que se encargara de crear la tarea segun el usuario."""
        pass
    
    async def add_job(self, programmed_task, id_task: str, date_object: datetime):
        """[method] Agrega el job (tarea) para que se ejecute en una fecha específica."""
        if self.active:
            scheduler.add_job(programmed_task, "date", run_date=date_object, id=id_task)
    
    async def remove_job_by_id(self, id_task: str):
        """[method]: Elimina el job (tarea) de acuerdo a su id (uuid del package) proporcionado."""
        if self.active:
            scheduler.remove_job(id_task)
    