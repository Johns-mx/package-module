"""
Este sistema de package permitira que se guarden datos en el campo "package", estos datos se guardaran en un archivo en caso de no tener conexion a internet, de lo contrario, los datos en "package" se enviaran al lugar establecido en "to".

Modelo de Package:
    - idPackage: int (uuid)*
    - date: datetime*
    - name: str *
    - from: str (path)*
    - destiny: str (path)*
    - actions: list[str]*
    - package: json (data)*

Banco de acciones:
: Este BPA es un archivo .json con el mismo nombre. El cual va a contener los packages pendientes (offline) que se enviaran al destino en cuanto se conecte a internet (online).
"""


### BANCO DE ACCIONES PENDIENTES (Bank of Pending Actions = BPA)
#Este ABk es un archivo .json con el mismo nombre.

