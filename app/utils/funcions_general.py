from datetime import datetime
import yaml
import os
import numpy as np




class ConfigManager:
    def __init__(self, config_paths):
        self.config_data = {}
        for path in config_paths:
            self.load_config(path)

    def load_config(self, path):
        with open(path, 'r', encoding='utf-8') as stream:
            try:
                config = yaml.safe_load(stream)
                self.config_data.update(config)
            except yaml.YAMLError as exc:
                print(exc)

    def get(self, key, default=None):
        if isinstance(key, str):
            return self.config_data.get(key, default)
        elif isinstance(key, list):
            val = self.config_data.get(key[0], default)
            for k in key[1:]:
                val = val.get(k, default)
            return val
        # return self.config_data.get(key, default)

