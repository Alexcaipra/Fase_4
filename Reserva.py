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
        """Solicita al servicio el cálculo del costo y lo almacena."""
        if self.validar_reserva():
            self.__costo_total = self.__servicio.calcular_costo()
            return self.__costo_total
        else:
            raise ValueError("No se pudo calcular el costo: Reserva inválida.")

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

    def cancelar_reserva(self):
        """Cancela la reserva si todavía no ha sido cancelada."""
        if self.__estado !="Cancelada":
            self.__estado = "Cancelada"
            return True
        return False
            

if __name__ == "__main__":

    from Cliente import Cliente
    from Servicio import AlquilerEquipo

    # Crear cliente de prueba
    cliente = Cliente("Carlos Pérez", "1234567890", "3001234567")

    # Crear servicio de prueba (opción y duración)
    servicio = AlquilerEquipo("Proyector", 2)

    # Crear reserva
    reserva = Reserva(cliente, servicio)

    # Prueba de validación
    print("\n--- PRUEBA DE VALIDACIÓN ---")
    print("Reserva válida:", reserva.validar_reserva())
    print("\n--- PRUEBA DE CÁLCULO ---")
    print("Costo calculado:", reserva.calcular_total())
    print("\n--- PRUEBA DE CONFIRMACIÓN ---")
    print("Reserva confirmada:", reserva.confirmar_reserva())
    print("\n--- PRUEBA DE CANCELACIÓN ---")
    print("Reserva cancelada:", reserva.cancelar_reserva())
    print("Cancelar nuevamente:", reserva.cancelar_reserva())
    print("\n--- PRUEBA DEL RESUMEN ---")
    reserva.mostrar_resumen()   

    print("\n--- PRUEBAS NEGATIVAS ---")

    # Reserva sin cliente
    reserva_sin_cliente = Reserva(None, servicio)
    print("Reserva sin cliente:", reserva_sin_cliente.validar_reserva())

    # Reserva sin servicio
    reserva_sin_servicio = Reserva(cliente, None)
    print("Reserva sin servicio:", reserva_sin_servicio.validar_reserva())

    # Intentar calcular costo de una reserva inválida
    try:
        reserva_sin_cliente.calcular_total()
    except ValueError as error:
        print("Error capturado:", error)
    pass