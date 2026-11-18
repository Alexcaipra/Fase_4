"""
Programa principal - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Estudiante 4: menú y coordinación del flujo principal.
"""




def cargar_clases():
    """Importa las clases de Cliente y los tres servicios especializados."""
    try:
        from cliente import Cliente
        from AlquilerEquipo import AlquilerEquipo
        from AsesoriaEspecializada import AsesoriaEspecializada
        from ReservaSala import ReservaSala
        return Cliente, AlquilerEquipo, AsesoriaEspecializada, ReservaSala
    except ImportError as error:
        raise ImportError(
            "Faltan módulos del proyecto o sus nombres no coinciden. "
            "Se requieren cliente.py, AlquilerEquipo.py, "
            "AsesoriaEspecializada.py y ReservaSala.py."
        ) from error


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
    Cliente, _, _, _ = cargar_clases()

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
    opcion = leer_opcion("Seleccione una categoría: ", 1, 3)
    categorias = {
        1: "alquiler",
        2: "asesoria",
        3: "sala"
    }
    return categorias[opcion]


def _consultar_opciones(servicio, categoria):
    """
    Consulta la lista de opciones de un servicio.
    Se contemplan nombres habituales porque la guía no fija el nombre
    exacto de estos métodos.
    """
    posibles = {
        "alquiler": (
            "consultar_equipos_disponibles",
            "consultar_equipos",
            "equipos_disponibles"
        ),
        "asesoria": (
            "consultar_asesorias_disponibles",
            "consultar_asesorias",
            "asesorias_disponibles"
        ),
        "sala": (
            "consultar_salas_disponibles",
            "consultar_salas",
            "salas_disponibles"
        )
    }

    for nombre in posibles[categoria]:
        atributo = getattr(servicio, nombre, None)
        if callable(atributo):
            resultado = atributo()
            if isinstance(resultado, (list, tuple)) and resultado:
                return list(resultado)
        elif isinstance(atributo, (list, tuple)) and atributo:
            return list(atributo)

    raise AttributeError(
        "La clase de servicio debe ofrecer un método o atributo para "
        "consultar sus opciones disponibles."
    )


def crear_servicio(categoria, opcion):
    """Construye el objeto especializado correspondiente a la categoría."""
    _, AlquilerEquipo, AsesoriaEspecializada, ReservaSala = cargar_clases()

    clases = {
        "alquiler": AlquilerEquipo,
        "asesoria": AsesoriaEspecializada,
        "sala": ReservaSala
    }
    clase = clases[categoria]

    # La implementación esperada recibe la opción seleccionada.
    # Si el constructor del compañero es diferente, ajustar esta línea.
    return clase(opcion)


def mostrar_servicios_disponibles(categoria):
    """Muestra los servicios de la categoría y devuelve el objeto elegido."""
    servicio_base = crear_servicio(categoria, None)
    opciones = _consultar_opciones(servicio_base, categoria)

    print("\n--- SERVICIOS DISPONIBLES ---")
    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion}")

    seleccion = leer_opcion("Seleccione un servicio: ", 1, len(opciones))
    return crear_servicio(categoria, opciones[seleccion - 1])


def solicitar_duracion():
    """Solicita la duración en horas y valida que sea mayor que cero."""
    while True:
        try:
            duracion = float(input("Ingrese la duración en horas: "))
            if duracion > 0:
                return duracion
            print("La duración debe ser mayor que cero.")
        except ValueError:
            print("Ingrese un número válido. Ejemplo: 2 o 1.5.")


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

            reserva = Reserva(cliente, servicio, duracion)
            if not reserva.validar_reserva():
                print("La reserva no cumple las condiciones requeridas.")
                continue

            costo = reserva.calcular_total()
            mostrar_cotizacion(servicio, duracion, costo)

            if solicitar_confirmacion():
                reserva.mostrar_resumen()
                print("Reserva confirmada correctamente.")
            else:
                print("La operación fue cancelada. No se registró la reserva.")

        except (ImportError, AttributeError, TypeError, ValueError) as error:
            print(f"Ocurrió un problema al procesar la reserva: {error}")
            print("Verifique la integración de las clases y vuelva a intentarlo.")

        continuar = input("\n¿Desea realizar otra reserva? (S/N): ").strip().lower()
        if continuar not in ("s", "si", "sí"):
            print("Programa finalizado. Gracias por utilizar el sistema.")
            break


if __name__ == "__main__":
    try:
        ejecutar_programa()
    except ImportError as error:
        print(f"No se pudo iniciar el programa: {error}")
