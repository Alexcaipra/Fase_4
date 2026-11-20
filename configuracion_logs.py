
import logging

# Configuración general del registro de eventos.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

# Creación del registrador del sistema.
logger = logging.getLogger("SistemaGestion")
