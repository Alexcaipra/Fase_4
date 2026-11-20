

# ============================================================
# ARCHIVO: manejo_errores.py
# OBJETIVO: Controlar los errores y registrar los eventos.
# ============================================================

from configuracion_logs import logger
from excepciones import ErrorSistema


def validar_duracion(duracion):
    """
    Verifica que la duración ingresada sea un número
    mayor que cero.
    """

    try:
        duracion = float(duracion)

        if duracion <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

    except ValueError as error:
        logger.error("Error al validar la duración: %s", error)

        # Encadena el error original con nuestra excepción.
        raise ErrorSistema(
            "No se pudo validar la duración."
        ) from error

    else:
        logger.info("Duración validada correctamente: %s horas", duracion)
        return duracion

    finally:
        logger.info("Finalizó el proceso de validación de duración.")


def ejecutar_operacion(operacion, descripcion):
    """
    Ejecuta una operación y controla los posibles errores.
    """

    logger.info("Iniciando operación: %s", descripcion)

    try:
        resultado = operacion()

    except ErrorSistema as error:
        logger.error("Error del sistema en %s: %s", descripcion, error)
        raise

    except Exception as error:
        logger.exception("Error inesperado en %s", descripcion)

        raise ErrorSistema(
            "Ocurrió un error inesperado durante la operación."
        ) from error

    else:
        logger.info("Operación realizada correctamente: %s", descripcion)
        return resultado

    finally:
        logger.info("Finalizó la operación: %s", descripcion)
