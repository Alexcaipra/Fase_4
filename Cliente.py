
# Importa la clase abstracta Entidad para establecer la herencia.
from Entidad import Entidad

# Clase Cliente que hereda de Entidad.
class Cliente(Entidad):
    """
    Clase encargada de representar a un cliente del sistema.
    Almacena sus datos personales y permite consultarlos y validarlos.
    """

    def __init__(self, nombre_cliente, numero_identificacion, numero_celular):
        # Inicializa los atributos privados del cliente.
        self.__nombre_cliente = nombre_cliente
        self.__numero_identificacion = numero_identificacion
        self.__numero_celular = numero_celular

    # Métodos getters: permiten acceder a los valores de los atributos privados.

    def get_nombre_cliente(self):
        return self.__nombre_cliente

    def get_numero_identificacion(self):
        return self.__numero_identificacion

    def get_numero_celular(self):
        return self.__numero_celular

    def validar_datos(self):
        """
        Comprueba que el nombre, la identificación y el celular
        cumplan con las condiciones establecidas.

        Retorna:
            True: si todos los datos son válidos.
            False: si se encuentra al menos un dato incorrecto.
        """

        # Se asume inicialmente que todos los datos son válidos.
        datos_validos = True

        # Validación del nombre del cliente.
        if not isinstance(self.__nombre_cliente, str):
            print("El nombre debe ser texto.")
            datos_validos = False

        elif not self.__nombre_cliente.strip():
            print("El nombre no puede estar vacío.")
            datos_validos = False

        elif any(caracter.isdigit() for caracter in self.__nombre_cliente):
            print("El nombre no puede contener números.")
            datos_validos = False

        # Validación del número de identificación.
        if not isinstance(self.__numero_identificacion, str):
            print("La identificación debe ser texto.")
            datos_validos = False

        elif not self.__numero_identificacion.strip():
            print("La identificación no puede estar vacía.")
            datos_validos = False

        elif not self.__numero_identificacion.isdigit():
            print("La identificación solo debe contener números.")
            datos_validos = False

        # Validación del número de celular.
        if not isinstance(self.__numero_celular, str):
            print("El celular debe ser texto.")
            datos_validos = False

        elif not self.__numero_celular.strip():
            print("El celular no puede estar vacío.")
            datos_validos = False

        elif not self.__numero_celular.isdigit():
            print("El celular solo debe contener números.")
            datos_validos = False

        elif len(self.__numero_celular) != 10:
            print("El celular debe tener 10 dígitos.")
            datos_validos = False

        # Retorna el resultado general de todas las validaciones.
        return datos_validos
    
    def mostrar_informacion(self):
        """
        Muestra en pantalla la información personal del cliente:
        nombre, número de identificación y número de celular.
        """
        print(f"Nombre: {self.__nombre_cliente}")
        print(f"Identificación: {self.__numero_identificacion}")
        print(f"Celular: {self.__numero_celular}")
