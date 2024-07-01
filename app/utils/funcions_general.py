"""
    Este archivo contiene funciones generales que se utilizan en diferentes partes del proyecto. # noqa
"""

# import os
# from datetime import datetime

# import numpy as np
import yaml


class ConfigManager:
    """
    Clase para manejar la configuración de la aplicación.
    """

    def __init__(self, config_paths):
        """
        Inicializa la clase ConfigManager.
        """
        self.config_data = {}
        for path in config_paths:
            self.load_config(path)

    def load_config(self, path):
        """
        Carga la configuración de un archivo YAML.
        """
        with open(path, "r", encoding="utf-8") as stream:
            try:
                config = yaml.safe_load(stream)
                self.config_data.update(config)
            except yaml.YAMLError as exc:
                print(exc)

    def get(self, key, default=None):
        """
        Obtiene un valor de la configuración.
        """
        if isinstance(key, str):
            return self.config_data.get(key, default)
        elif isinstance(key, list):
            val = self.config_data
            for k in key:
                if isinstance(val, dict):
                    val = val.get(k, default)
                else:
                    return default
            return val
        else:
            return default
