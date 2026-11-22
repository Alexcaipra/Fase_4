"""
Programa principal - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Estudiante 4: menú y coordinación del flujo principal.
"""

import logging

logging.basicConfig(
    filename="reservas.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger(__name__)




def cargar_clases():
    """Importa las clases de Cliente y los tres servicios especializados."""
    try:
        from Cliente import Cliente
        from Reserva import Reserva
        from Servicio import AlquilerEquipo
        from Servicio import AsesoriaEspecializada
        from Servicio import ReservaSala
        

        return Cliente, Reserva, AlquilerEquipo, AsesoriaEspecializada, ReservaSala

    except ImportError as error:
        logger.exception("Error importando clases del sistema")
        raise ImportError("No se pudieron cargar las clases requeridas.") from error

def leer_texto(mensaje):
    """Solicita un texto no vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El dato no puede estar vacío. Intente nuevamente.")


def leer_opcion(mensaje, minimo, maximo):
    """Lee y valida una opción numérica dentro de un rango."""
    while True:
        try:
            opcion = int(input(mensaje))
            if minimo <= opcion <= maximo:
                return opcion
            print(f"Seleccione una opción entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")


def mostrar_menu_principal():
    """Presenta el menú inicial y devuelve la opción como texto."""
    print("\n==============================================")
    print(" SISTEMA INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS")
    print("==============================================")
    print("1. Realizar una reserva")
    print("2. Salir")
    return str(leer_opcion("Seleccione una opción: ", 1, 2))


def solicitar_datos_cliente():
    """Solicita los datos, crea el cliente y valida la información."""
    Cliente, _, _, _,_ = cargar_clases()

    print("\n--- DATOS DEL CLIENTE ---")
    nombre = leer_texto("Nombre completo: ")
    identificacion = leer_texto("Número de identificación: ")
    celular = leer_texto("Número de celular: ")

    try:
        cliente = Cliente(nombre, identificacion, celular)
        if cliente.validar_datos():
            return cliente
        print("Los datos del cliente no son válidos.")
        return None
    except (TypeError, ValueError) as error:
        print(f"No fue posible registrar el cliente: {error}")
        return None


def mostrar_categorias_servicios():
    """Muestra las tres categorías y devuelve la categoría seleccionada."""
    print("\n--- CATEGORÍAS DE SERVICIOS ---")
    print("1. Alquiler de equipos")
    print("2. Asesoría especializada")
    print("3. Reserva de salas")
    opcion = leer_opcion("Seleccione una categoría: ", 1,3)
    categorias = {
        1: "alquiler",
        2: "asesoria",
        3: "sala"
    }
    return categorias[opcion]


def mostrar_servicios_disponibles(categoria): 
    
    """Muestra los servicios disponibles con su tarifa por hora."""

    Cliente, Reserva, AlquilerEquipo, AsesoriaEspecializada, ReservaSala = cargar_clases()
    
    catalogos = {
        "alquiler": AlquilerEquipo.equipos,
        "asesoria": AsesoriaEspecializada.asesorias,
        "sala": ReservaSala.salas
    }

    catalogo = catalogos[categoria]

    print("\n--- SERVICIOS DISPONIBLES ---")
    for indice, (nombre, precio) in enumerate(catalogo.items(), start=1):
        print(f"{indice}. {nombre} - ${precio:,.0f} por hora")

    seleccion = leer_opcion("Seleccione un servicio: ", 1, len(catalogo))

    opciones = list(catalogo.keys())

    return opciones[seleccion - 1]
       
    

def solicitar_duracion():
    """Solicita la duración en horas; permite cancelar con C."""
    while True:
        print("\n----------------------------------------")
        print("          DURACIÓN DEL SERVICIO")
        print("----------------------------------------")
        print("Ingrese la duración en horas.")
        print("Escriba C para cancelar la operación.\n")
        entrada = input("Duración: ").strip().lower()
        
        if entrada == "c":
            return None

        try:
            duracion = float(entrada)
            if duracion > 0:
                return duracion
            print("La duración debe ser mayor que cero.")
        except ValueError:
            print("Ingrese un número válido. Ejemplo: 2 o 1.5.")


def crear_servicio(categoria, opcion, duracion):
    """Construye el objeto especializado correspondiente a la categoría."""
    _, _, AlquilerEquipo, AsesoriaEspecializada, ReservaSala = cargar_clases()

    clases = {
        "alquiler": AlquilerEquipo,
        "asesoria": AsesoriaEspecializada,
        "sala": ReservaSala
    }
    clase = clases[categoria]

    # La implementación esperada recibe la opción seleccionada.
    # Si el constructor del compañero es diferente, ajustar esta línea.
    return clase(opcion, duracion)


def mostrar_cotizacion(servicio, duracion, costo):
    """Presenta el servicio, la duración y el costo estimado."""
    print("\n========== COTIZACIÓN ==========")
    print(f"Servicio: {servicio.describir_servicio()}")
    print(f"Duración: {duracion:.2f} horas")
    print(f"Costo total: ${costo:,.2f}")
    print("================================")


def solicitar_confirmacion():
    """Pregunta si se confirma la reserva y devuelve True o False."""
    while True:
        respuesta = input("¿Desea confirmar la reserva? (S/N): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Respuesta no válida. Escriba S para sí o N para no.")


def ejecutar_programa():
    """Coordina el proceso completo y permite realizar varias reservas."""
    print("Bienvenido al sistema de gestión de reservas.")

    while True:
        opcion = mostrar_menu_principal()

        if opcion == "2":
            print("Gracias por utilizar el sistema. ¡Hasta pronto!")
            break

        cliente = solicitar_datos_cliente()
        if cliente is None:
            print("No se puede continuar con datos de cliente inválidos.")
            continue

        try:
            
            categoria = mostrar_categorias_servicios()
            servicio = mostrar_servicios_disponibles(categoria)
            duracion = solicitar_duracion()

            if duracion is None:
                print("Reserva cancelada por el usuario. Regresando al menú principal.")
                logger.info("Usuario canceló al ingresar la duración")
                continue
            
            _, Reserva, _, _, _ = cargar_clases()

            servicio = crear_servicio(categoria, servicio, duracion)

            reserva = Reserva(cliente, servicio)
            if not reserva.validar_reserva():
                print("La reserva no cumple las condiciones requeridas.")
                continue

            costo = reserva.calcular_total()
            mostrar_cotizacion(servicio, duracion, costo)

            if solicitar_confirmacion():
                if reserva.confirmar_reserva():
                    reserva.mostrar_resumen()
                    print(f"Reserva {reserva.obtener_estado()} correctamente.")
                    logger.info("Reserva confirmada. Servicio=%s costo=%s", servicio.describir_servicio(), costo)
                else:
                    print("No fue posible confirmar la reserva.")
                    logger.warning("No se pudo confirmar reserva; estado=%s", reserva.obtener_estado())
            else:
                reserva.rechazar_reserva()
                print(f"Reserva {reserva.obtener_estado().lower()}. No se registró la reserva.")
                logger.info("Reserva rechazada por el usuario. Servicio=%s", servicio.describir_servicio())

        except (ImportError, AttributeError, TypeError, ValueError) as error:
            logger.exception("Error durante el proceso de reserva")
            print(f"Ocurrió un problema al procesar la reserva: {error}")
            print("Verifique la integración de las clases y vuelva a intentarlo.")
        else:
            logger.info("Flujo de reserva finalizado sin excepciones")

        finally:
            logger.info("Finalizó un intento de reserva")

        continuar = input("\n¿Desea realizar otra reserva? (S/N): ").strip().lower()
        if continuar not in ("s", "si", "sí"):
            print("Programa finalizado. Gracias por utilizar el sistema.")
            break


if __name__ == "__main__":
    try:
        ejecutar_programa()
    except ImportError as error:
        print(f"No se pudo iniciar el programa: {error}")
