"""
    format_logger.py:
        Este módulo contiene la definición de la clase ColoredFormatter que se encarga de dar formato
        a los mensajes de log con colores.
"""

import logging

from termcolor import colored


class ColoredFormatter(logging.Formatter):
    """
    Clase para dar formato a los mensajes de log con colores
    """

    COLORS = {
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    }

    def format(self, record):
        """
        Función para dar formato a los mensajes de log con colores
        """
        log_message = super().format(record)
        if record.levelname == "CRITICAL":
            return colored(
                log_message, self.COLORS.get(record.levelname), attrs=["bold"]
            )
        return colored(log_message, self.COLORS.get(record.levelname))


def def_log(path_log: str = "./", file: str = "log.log"):
    """
    Description:
    ------------
    Función para definir el formato del logger

    Parameters:
    -----------
    path_log: str
        Path del archivo de log

    Returns:
    --------
    logger: logging.Logger
        Logger con el formato definido


    Example:
    --------
    >>> logger = def_log(path_log='log.log')
    >>> logger.debug("Esto es un mensaje DEBUG")
    >>> logger.info("Esto es un mensaje INFO")
    >>> logger.warning("Esto es un mensaje WARNING")
    >>> logger.error("Esto es un mensaje ERROR")
    >>> logger.critical("Este es un mensaje CRITICAL")

    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Manejador para la consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter_console = ColoredFormatter(
        "%(asctime)s  %(levelname)-8s(%(name)s):     %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter_console)

    # Manejador para el archivo de registro
    file_handler = logging.FileHandler(
        path_log + file, encoding="utf-8"
    )  # Cambia 'archivo_de_registro.log' al nombre de tu archivo de registro
    file_handler.setLevel(logging.DEBUG)

    formatter_file = logging.Formatter(
        "%(asctime)s  %(levelname)-8s(%(name)s):     %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter_file)

    # Añadir los manejadores solo si no hay manejadores configurados
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(file_handler)
    else:
        # Eliminar todos los manejadores y añadir los nuevos
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.addHandler(ch)
        logger.addHandler(file_handler)
    return logger


# # Realizar algunas llamadas de registro para probarlo
# logger.debug("Esto es un mensaje DEBUG")
# logger.info("Esto es un mensaje INFO")
# logger.warning("Esto es un mensaje WARNING")
# logger.error("Esto es un mensaje ERROR")
# logger.critical("Este es un mensaje CRITICAL")
