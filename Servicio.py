from abc import ABC, abstractmethod
from Entidad import Entidad

class Servicio(Entidad, ABC):
    """
    Clase abstracta que representa un servicio general.
    Hereda de Entidad.
    """
    def __init__(self, duracion):

        # Almacena la duración del servicio en horas.
        self.duracion = duracion
   
    @abstractmethod
    def calcular_costo(self):
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

    def obtener_duracion(self):
        #retorna la duraccion del servicio en horas
        return self.duracion


class AlquilerEquipo(Servicio):
    def __init__(self, opcion_seleccionada, duracion):
        super().__init__(duracion)
        self.opcion_seleccionada = opcion_seleccionada
        self.duracion = duracion

        # Diccionario con equipos y precios
        self.equipos = { 
            "Cámara de video": 25000, "Proyector": 15000, "Laptop HP": 20000, "Micrófono": 8000, "Consola": 18000
            }

    def validar_parametros(self):
            #Verifica si el equipo seleccionado existe en el diccionario
            return self.opcion_seleccionada in self.equipos

    def describir_servicio(self):
        #Retorna la descripción del alquiler del equipo seleccionado
        return f"Alquiler de {self.opcion_seleccionada}"        

    def calcular_costo(self):
        #Calcula el costo del alquiler según la tarifa y la duración
        if self.validar_parametros():
            precio = self.equipos[self.opcion_seleccionada]
            return precio * self.duracion

        return 0.0
    
    def consultar_equipos_disponibles(self):
        #Retorna el catálogo de equipos con sus tarifas por hora
        return self.equipos
    


class AsesoriaEspecializada(Servicio):
    def __init__(self, opcion_seleccionada, duracion):
        super().__init__(duracion)
        self.opcion_seleccionada = opcion_seleccionada
        self.duracion = duracion

        ## Diccionario con asesorias y precios
        self.asesorias = {
            "Asesoría en programación": 40000, "Asesoría en electrónica": 35000, "Asesoría en automatización": 50000, 
            "Asesoría en redes": 30000, "Asesoría en instrumentación industrial": 45000
            }

    def validar_parametros(self):
        #Verifica si la asesoria seleccionada existe en el diccionario
        return self.opcion_seleccionada in self.asesorias

    def describir_servicio(self):
           #Retorna la descripción de la asesoria seleccionado
           return self.opcion_seleccionada
             
    def calcular_costo(self):
        #Calcula el costo de la asesoria según la tarifa y la duración
        if self.validar_parametros():
            precio = self.asesorias[self.opcion_seleccionada]
            return precio*self.duracion
        return 0.0

    def consultar_asesorias_disponibles(self):
         #Retorna el catálogo de asesorias con sus tarifas por hora
        return self.asesorias


class ReservaSala(Servicio):
    def __init__(self, opcion_seleccionada, duracion):
        super().__init__(duracion)
        self.opcion_seleccionada = opcion_seleccionada
        self.duracion = duracion

        ## Diccionario con salas y precios
        self.salas = {
            "Sala Grande": 80000, "Sala Pequeña": 40000, "Sala VIP": 100000, "Sala de Juntas": 60000, 
            "Auditorio": 150000
            }

    def validar_parametros(self):
        #Verifica si la sala seleccionada existe en el diccionario
        return self.opcion_seleccionada in self.salas

    def describir_servicio(self):
        #Retorna la descripción de la sala seleccionada
        return self.opcion_seleccionada

    def calcular_costo(self):
        #Calcula el costo del alquiler de la sala según la tarifa y la duración
        if self.validar_parametros():
            precio = self.salas[self.opcion_seleccionada]
            return precio*self.duracion
        return 0.0
        
    def consultar_salas_disponibles(self):
         #Retorna el catálogo de salas con sus tarifas por hora
        return self.salas

    


   