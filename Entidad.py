
# Importa las herramientas necesarias para crear clases abstractas.
from abc import ABC, abstractmethod


class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Sirve como clase padre para las clases Cliente y Servicio.
    """

    @abstractmethod
    def mostrar_informacion(self):
        """
        Método abstracto que obliga a las clases hijas a implementar
        su propia forma de mostrar la información.
        """
        pass