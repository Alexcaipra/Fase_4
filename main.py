"""UNAD - Programación 213023 | Fase 4 - Software FJ.
Sistema de clientes, servicios y reservas, sin bases de datos.
"""
from abc import ABC, abstractmethod
import logging
import math

# Archivo de eventos y errores (si el entorno permite crear archivos).
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)
if not logger.handlers:
    try:
        manejador = logging.FileHandler("fase4_eventos.log", encoding="utf-8")
    except OSError:
        manejador = logging.StreamHandler()
    manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(manejador)


class ErrorSistema(Exception):
    """Error general de la aplicación."""


class ErrorValidacion(ErrorSistema):
    """Datos que no cumplen las reglas."""


class ErrorDisponibilidad(ErrorSistema):
    """Servicio no disponible."""


class ErrorReserva(ErrorSistema):
    """Operación de reserva no permitida."""


def texto_obligatorio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorValidacion(f"{campo} debe tener un texto válido.")
    return valor.strip()


def numero_positivo(valor, campo):
    if isinstance(valor, bool):
        raise ErrorValidacion(f"{campo} debe ser un número positivo.")
    try:
        numero = float(valor)
    except (TypeError, ValueError) as error:
        raise ErrorValidacion(f"{campo} debe ser numérico.") from error
    if not math.isfinite(numero) or numero <= 0:
        raise ErrorValidacion(f"{campo} debe ser mayor que cero.")
    return numero


def porcentaje(valor, campo):
    if isinstance(valor, bool):
        raise ErrorValidacion(f"{campo} debe estar entre 0 y 100.")
    try:
        numero = float(valor)
    except (ValueError, TypeError) as error:
        raise ErrorValidacion(f"{campo} debe ser numérico.") from error
    if not math.isfinite(numero) or not 0 <= numero <= 100:
        raise ErrorValidacion(f"{campo} debe estar entre 0 y 100.")
    return numero


class Entidad(ABC):
    @abstractmethod
    def mostrarInformacion(self):
        pass


class Cliente(Entidad):
    def __init__(self, nombre, identificacion, celular):
        self.__nombre = texto_obligatorio(nombre, "Nombre")
        documento = str(identificacion).strip()
        telefono = str(celular).strip()
        if not documento.isdigit() or not 5 <= len(documento) <= 15:
            raise ErrorValidacion("La identificación debe tener entre 5 y 15 dígitos.")
        if not telefono.isdigit() or len(telefono) != 10:
            raise ErrorValidacion("El celular debe tener 10 dígitos.")
        self.__identificacion = documento
        self.__celular = telefono

    @property
    def identificacion(self):
        return self.__identificacion

    def validarDatos(self):
        return True

    def mostrarInformacion(self):
        return f"Cliente: {self.__nombre} | ID: {self.__identificacion} | Cel: {self.__celular}"


class Servicio(Entidad, ABC):
    def __init__(self, tarifaPorHora, disponible=True):
        self._tarifaPorHora = numero_positivo(tarifaPorHora, "Tarifa por hora")
        if not isinstance(disponible, bool):
            raise ErrorValidacion("La disponibilidad debe ser True o False.")
        self._disponible = disponible

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ErrorValidacion("La disponibilidad debe ser True o False.")
        self._disponible = valor

    def _costo_ajustado(self, duracion, impuesto=0, descuento=0):
        horas = numero_positivo(duracion, "Duración")
        iva = porcentaje(impuesto, "Impuesto")
        rebaja = porcentaje(descuento, "Descuento")
        if not self.disponible:
            raise ErrorDisponibilidad("El servicio no está disponible.")
        subtotal = self._tarifaPorHora * horas
        return round(subtotal * (1 - rebaja / 100) * (1 + iva / 100), 2)

    @abstractmethod
    def calcularCosto(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describirServicio(self):
        pass

    @abstractmethod
    def validarParametros(self):
        pass

    def mostrarInformacion(self):
        return self.describirServicio()


class AlquilerEquipo(Servicio):
    def __init__(self, nombreEquipo, referencia, tarifaPorHora, disponible=True):
        super().__init__(tarifaPorHora, disponible)
        self.nombreEquipo = texto_obligatorio(nombreEquipo, "Nombre del equipo")
        self.referencia = texto_obligatorio(referencia, "Referencia")
        self.validarParametros()

    def validarParametros(self):
        return bool(self.nombreEquipo and self.referencia)

    def calcularCosto(self, duracion, impuesto=0, descuento=0):
        return self._costo_ajustado(duracion, impuesto, descuento)

    def describirServicio(self):
        return f"Alquiler de equipo: {self.nombreEquipo} ({self.referencia})"


class AsesoriaEspecializada(Servicio):
    def __init__(self, tipoAsesoria, tarifaPorHora, disponible=True):
        super().__init__(tarifaPorHora, disponible)
        self.tipoAsesoria = texto_obligatorio(tipoAsesoria, "Tipo de asesoría")
        self.validarParametros()

    def validarParametros(self):
        return bool(self.tipoAsesoria)

    def calcularCosto(self, duracion, impuesto=0, descuento=0):
        return self._costo_ajustado(duracion, impuesto, descuento)

    def describirServicio(self):
        return f"Asesoría especializada: {self.tipoAsesoria}"


class ReservaSala(Servicio):
    def __init__(self, tipoSala, tarifaPorHora, disponible=True):
        super().__init__(tarifaPorHora, disponible)
        self.tipoSala = texto_obligatorio(tipoSala, "Tipo de sala")
        self.validarParametros()

    def validarParametros(self):
        return bool(self.tipoSala)

    def calcularCosto(self, duracion, impuesto=0, descuento=0):
        return self._costo_ajustado(duracion, impuesto, descuento)

    def describirServicio(self):
        return f"Reserva de sala: {self.tipoSala}"


class Reserva:
    def __init__(self, cliente, servicio, duracion, impuesto=0, descuento=0):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Debes indicar un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Debes indicar un servicio válido.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = numero_positivo(duracion, "Duración")
        self.impuesto = porcentaje(impuesto, "Impuesto")
        self.descuento = porcentaje(descuento, "Descuento")
        self.estado = "pendiente"
        self.total = 0.0

    def procesarReserva(self):
        try:
            if self.estado != "pendiente":
                raise ErrorReserva("Solo se procesan reservas pendientes.")
            self.total = self.servicio.calcularCosto(
                self.duracion, self.impuesto, self.descuento
            )
        except ErrorSistema as error:
            raise ErrorReserva("No se pudo procesar la reserva: " + str(error)) from error
        else:
            self.estado = "confirmada"
            logger.info("Reserva confirmada | %s | Total: %.2f", self.servicio.describirServicio(), self.total)
            return self.total
        finally:
            logger.info("Procesamiento revisado | Estado: %s", self.estado)

    def confirmar(self):
        return self.procesarReserva()

    def cancelar(self):
        if self.estado == "cancelada":
            raise ErrorReserva("Esta reserva ya está cancelada.")
        if self.estado != "confirmada":
            raise ErrorReserva("Solo se cancelan reservas confirmadas.")
        self.estado = "cancelada"
        logger.info("Reserva cancelada: %s", self.servicio.describirServicio())
        return "Reserva cancelada correctamente"


class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrarCliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("Solo se admiten objetos Cliente.")
        if any(c.identificacion == cliente.identificacion for c in self.clientes):
            raise ErrorValidacion("Ya existe un cliente con esa identificación.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.identificacion)
        return cliente.mostrarInformacion()

    def registrarServicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ErrorValidacion("Solo se admiten objetos Servicio.")
        servicio.validarParametros()
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.describirServicio())
        return servicio.describirServicio()

    def crearReserva(self, cliente, servicio, duracion, impuesto=0, descuento=0):
        if cliente not in self.clientes:
            raise ErrorReserva("El cliente no está registrado.")
        if servicio not in self.servicios:
            raise ErrorReserva("El servicio no está registrado.")
        reserva = Reserva(cliente, servicio, duracion, impuesto, descuento)
        reserva.confirmar()
        self.reservas.append(reserva)
        return f"Reserva {reserva.estado} | Total: ${reserva.total:,.2f}"

    def resumen(self):
        print("\n" + "=" * 55)
        print("RESUMEN DEL SISTEMA SOFTWARE FJ")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Servicios registrados: {len(self.servicios)}")
        print(f"Reservas registradas: {len(self.reservas)}")
        for numero, reserva in enumerate(self.reservas, start=1):
            print(f"  {numero}. {reserva.servicio.describirServicio()} | "
                  f"{reserva.estado} | ${reserva.total:,.2f}")
        print("Los errores y eventos se registran en fase4_eventos.log")
        print("=" * 55)


def main():
    sistema = SistemaGestion()
    resultados = {"correctas": 0, "controladas": 0}

    def prueba(numero, descripcion, operacion):
        print(f"\nPRUEBA {numero:02d} - {descripcion}")
        try:
            resultado = operacion()
        except ErrorSistema as error:
            resultados["controladas"] += 1
            print("  ERROR CONTROLADO:", error)
            logger.exception("Prueba %s: %s", numero, descripcion)
        except Exception:
            resultados["controladas"] += 1
            print("  ERROR INESPERADO CONTROLADO; el programa continúa.")
            logger.exception("Error inesperado en prueba %s", numero)
        else:
            resultados["correctas"] += 1
            print("  OK:", resultado)
        finally:
            print("  Prueba terminada. El sistema sigue funcionando.")

    print("UNAD | FASE 4 - PROGRAMACIÓN 213023")
    print("SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")

    # Los objetos existen únicamente en memoria (listas), sin bases de datos.
    ana = Cliente("Ana Torres", "100200300", "3001234567")
    luis = Cliente("Luis Pérez", "100200301", "3109876543")
    sala = ReservaSala("Sala de reuniones", 50000)
    equipo = AlquilerEquipo("Portátil", "HP-01", 40000)
    asesoria = AsesoriaEspecializada("Seguridad informática", 80000)

    prueba(1, "Registrar a Ana", lambda: sistema.registrarCliente(ana))
    prueba(2, "Registrar a Luis", lambda: sistema.registrarCliente(luis))
    prueba(3, "Rechazar cliente sin nombre", lambda: sistema.registrarCliente(Cliente(" ", "100200302", "3201234567")))
    prueba(4, "Rechazar celular incorrecto", lambda: sistema.registrarCliente(Cliente("Eva", "100200303", "123")))
    prueba(5, "Rechazar identificación duplicada", lambda: sistema.registrarCliente(Cliente("Otra Ana", "100200300", "3201234567")))
    prueba(6, "Registrar sala", lambda: sistema.registrarServicio(sala))
    prueba(7, "Registrar alquiler de equipo", lambda: sistema.registrarServicio(equipo))
    prueba(8, "Registrar asesoría", lambda: sistema.registrarServicio(asesoria))
    prueba(9, "Rechazar tarifa negativa", lambda: sistema.registrarServicio(ReservaSala("Sala X", -200)))
    prueba(10, "Rechazar servicio sin nombre", lambda: sistema.registrarServicio(AlquilerEquipo("", "REF-1", 5000)))
    prueba(11, "Reservar sala por 2 horas con 19% de impuesto", lambda: sistema.crearReserva(ana, sala, 2, impuesto=19))
    prueba(12, "Reservar equipo por 3 horas con 10% de descuento", lambda: sistema.crearReserva(luis, equipo, 3, descuento=10))
    prueba(13, "Reservar asesoría por 1.5 horas", lambda: sistema.crearReserva(ana, asesoria, 1.5))
    prueba(14, "Rechazar duración cero", lambda: sistema.crearReserva(ana, sala, 0))
    prueba(15, "Rechazar servicio inexistente", lambda: sistema.crearReserva(ana, "otro", 2))
    prueba(16, "Rechazar impuesto mayor al 100%", lambda: sistema.crearReserva(ana, sala, 2, impuesto=120))
    prueba(17, "Cancelar una reserva confirmada", lambda: sistema.reservas[0].cancelar())
    prueba(18, "Rechazar segunda cancelación", lambda: sistema.reservas[0].cancelar())
    prueba(19, "Marcar asesoría como no disponible", lambda: setattr(asesoria, "disponible", False) or "Servicio deshabilitado")
    prueba(20, "Rechazar reserva de servicio no disponible", lambda: sistema.crearReserva(luis, asesoria, 2))

    sistema.resumen()
    print(f"Pruebas ejecutadas: {sum(resultados.values())}")
    print(f"Operaciones correctas: {resultados['correctas']}")
    print(f"Errores controlados: {resultados['controladas']}")


if __name__ == "__main__":
    main()
