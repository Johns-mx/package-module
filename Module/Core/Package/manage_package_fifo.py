""" Sorting in Output Packages (SOP)
Los primeros paquetes serán los primeros en salir.

Este modulo se encarga de manejar los paquetes de acuerdo a su fecha de registro en BPA.
"""

from datetime import datetime


class SortPackageBPA:
    def __init__(self):
        self.package: dict