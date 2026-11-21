class Reserva:
    """
    Clase que gestiona las reservas, integrando un cliente y un servicio,
    y controlando su costo y estado.
    """
    def __init__(self, cliente, servicio):
        self.__cliente = cliente
        self.__servicio = servicio
        self.__costo_total = 0.0
        self.__estado = "Pendiente"

    def validar_reserva(self):
        """Verifica que el cliente y el servicio cumplan con sus validaciones"""
        if self.__cliente is None or self.__servicio is None:
            return False
        
        if not self.__cliente.validar_datos():
            return False
        # Verifica que el servicio tenga sus propios parámetros validados
        return self.__servicio.validar_parametros()
    

    def calcular_total(self):
        """Calcula y almacena el costo; lanza ValueError si la reserva no es valida."""
        if not self.validar_reserva():
            raise ValueError("No se pudo calcular el costo: reserva invalida.")
        costo = self.__servicio.calcular_costo()
        if costo is None or costo < 0:
            raise ValueError("El servicio devolvio un costo invalido.")
        self.__costo_total = costo
        return self.__costo_total


    def mostrar_resumen(self):
        """Muestra el resumen de la reserva con los datos del cliente y servicio"""
        print("\n--- RESUMEN DE LA RESERVA ---")
       
        self.__cliente.mostrar_informacion()
        print(f"Servicio: {self.__servicio.describir_servicio()}")
        print(f"Duración: {self.__servicio.obtener_duracion()} horas")
        print(f"Costo Total: ${self.__costo_total}")
        print("-----------------------------\n")

    def confirmar_reserva(self):
        """Confirma la reserva si está pendiente, es válida y tiene un costo calculado."""
        if self.__estado == "Pendiente" and self.validar_reserva() and self.__costo_total != 0.0:
            self.__estado = "Confirmada"
            return True
        return False

    def rechazar_reserva(self):
        """Rechaza una reserva que siga pendiente."""
        if self.__estado == "Pendiente":
            self.__estado = "Rechazada"
            return True
        return False

    def cancelar_reserva(self):
        """Cancela la reserva si todavía no ha sido cancelada."""
        if self.__estado !="Cancelada":
            self.__estado = "Cancelada"
            return True
        return False

    def obtener_estado(self):
        """Retorna el estado actual de la reserva."""
        return self.__estado
            

