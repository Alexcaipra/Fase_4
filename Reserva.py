class Reserva:
    """
    Clase que integra al cliente con el servicio.
    No hereda de Entidad.
    """
    def __init__(self, cliente, servicio, duracion):
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__costo_total = 0.0

    def validar_reserva(self):
        """Verifica que el cliente, el servicio y la duración sean válidos."""
        if self.__cliente is None or self.__servicio is None:
            return False
        if self.__duracion <= 0:
            return False
        # Verifica que el servicio tenga sus propios parámetros validados
        return self.__servicio.validar_parametros()

    def calcular_total(self):
        """Solicita al servicio el cálculo del costo y lo guarda."""
        if self.validar_reserva():
            self.__costo_total = self.__servicio.calcular_costo(self.__duracion)
            return self.__costo_total
        else:
            raise ValueError("No se pudo calcular el costo: Reserva inválida.")

    def mostrar_resumen(self):
        """Muestra en pantalla los datos del cliente, servicio y costo."""
        print("\n--- RESUMEN DE LA RESERVA ---")
        if hasattr(self.__cliente, 'mostrar_informacion'):
            self.__cliente.mostrar_informacion()
        
        print(f"Servicio: {self.__servicio.describir_servicio()}")
        print(f"Duración: {self.__duracion} horas")
        print(f"Costo Total: ${self.__costo_total}")
        print("-----------------------------\n")
