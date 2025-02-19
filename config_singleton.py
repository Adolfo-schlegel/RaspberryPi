# config_singleton.py
from config_handler import ConfigHandler

# Create a global instance that can be imported everywhere
config_handler_instance = ConfigHandler("config.json")

def get_config():
    return config_handler_instance
