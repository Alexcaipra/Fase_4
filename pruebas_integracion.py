
# ============================================================
# ARCHIVO: pruebas_integracion.py
# OBJETIVO: Comprobar el funcionamiento de los módulos
# de registro de eventos y manejo de excepciones.
# ============================================================

from configuracion_logs import logger
from manejo_errores import validar_duracion, ejecutar_operacion
from excepciones import ErrorSistema

def probar_duracion_valida():
    """Comprueba que se acepte una duración positiva."""

    resultado = validar_duracion(2.5)
    assert resultado == 2.5

    logger.info("PRUEBA SUPERADA: duración válida.")


def probar_duracion_invalida():
    """Comprueba que se rechacen duraciones no válidas."""

    try:
        validar_duracion(-3)

    except ErrorSistema:
        logger.info("PRUEBA SUPERADA: duración negativa rechazada.")

    else:
        raise AssertionError("No se rechazó la duración negativa.")


def probar_duracion_cero():
    """Comprueba que no se acepte una duración igual a cero."""

    try:
        validar_duracion(0)

    except ErrorSistema:
        logger.info("PRUEBA SUPERADA: duración cero rechazada.")

    else:
        raise AssertionError("No se rechazó la duración cero.")


def probar_operacion_exitosa():
    """Comprueba la ejecución correcta de una operación."""

    resultado = ejecutar_operacion(
        lambda: "Operación completada",
        "Prueba de operación exitosa"
    )

    assert resultado == "Operación completada"

    logger.info("PRUEBA SUPERADA: operación exitosa.")


def probar_error_inesperado():
    """Comprueba el control de errores inesperados."""

    def operacion_con_error():
        raise ZeroDivisionError("División entre cero.")

    try:
        ejecutar_operacion(
            operacion_con_error,
            "Prueba de error inesperado"
        )

    except ErrorSistema:
        logger.info("PRUEBA SUPERADA: error inesperado controlado.")

    else:
        raise AssertionError("No se controló el error inesperado.")


def ejecutar_pruebas():
    """Ejecuta todas las pruebas de integración."""

    logger.info("========== INICIO DE PRUEBAS ==========")

    probar_duracion_valida()
    probar_duracion_invalida()
    probar_duracion_cero()
    probar_operacion_exitosa()
    probar_error_inesperado()

    logger.info("========== PRUEBAS FINALIZADAS ==========")


if __name__ == "__main__":
    ejecutar_pruebas()
