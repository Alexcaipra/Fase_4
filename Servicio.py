from abc import ABC, abstractmethod
from Entidad import Entidad

class Servicio(Entidad, ABC):
    """
    Clase abstracta que representa un servicio general.
    Hereda de Entidad.
    """
    def __init__(self, tarifa_por_hora):
        self.tarifa_por_hora = tarifa_por_hora
        self.opcion_seleccionada = None

    @abstractmethod
    def calcular_costo(self, duracion):
        """Calcula el costo del servicio según la duración."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Devuelve el nombre específico del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Verifica que los parámetros del servicio sean válidos."""
        pass

    def mostrar_informacion(self):
        """Muestra la descripción del servicio."""
        print(f"Servicio: {self.describir_servicio()}")


class AlquilerEquipo(Servicio):
    def __init__(self, tarifa_por_hora):
        super().__init__(tarifa_por_hora)
        # Lista de 5 equipos disponibles
        self.equipos = ["Cámara de video", "Proyector", "Laptop HP", "Micrófono", "Consola"]

    def consultar_equipos_disponibles(self):
        return self.equipos

    def calcular_costo(self, duracion):
        if self.validar_parametros() and duracion > 0:
            return self.tarifa_por_hora * duracion
        return 0.0

    def describir_servicio(self):
        if self.opcion_seleccionada:
            return f"Alquiler de {self.opcion_seleccionada}"
        return "Alquiler de Equipo (No seleccionado)"

    def validar_parametros(self):
        return self.opcion_seleccionada in self.equipos


class AsesoriaEspecializada(Servicio):
    def __init__(self, tarifa_por_hora):
        super().__init__(tarifa_por_hora)
        # Lista de asesorías
        self.asesorias = ["Fotografía", "Programación", "Redes", "Bases de datos", "Marketing"]

    def consultar_asesorias_disponibles(self):
        return self.asesorias

    def calcular_costo(self, duracion):
        if self.validar_parametros() and duracion > 0:
            return self.tarifa_por_hora * duracion
        return 0.0

    def describir_servicio(self):
        if self.opcion_seleccionada:
            return f"Asesoría en {self.opcion_seleccionada}"
        return "Asesoría Especializada (No seleccionada)"

    def validar_parametros(self):
        return self.opcion_seleccionada in self.asesorias


class ReservaSala(Servicio):
    def __init__(self, tarifa_por_hora):
        super().__init__(tarifa_por_hora)
        # Lista de salas
        self.salas = ["Sala Grande", "Sala Pequeña", "Sala VIP", "Sala de Juntas", "Auditorio"]

    def consultar_salas_disponibles(self):
        return self.salas

    def calcular_costo(self, duracion):
        if self.validar_parametros() and duracion > 0:
            return self.tarifa_por_hora * duracion
        return 0.0

    def describir_servicio(self):
        if self.opcion_seleccionada:
            return f"Reserva de {self.opcion_seleccionada}"
        return "Reserva de Sala (No seleccionada)"

    def validar_parametros(self):
        return self.opcion_seleccionada in self.salas
      
