import json

class ConfigHandler:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Loads the config from the given file."""
        try:
            with open(self.config_path, "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print(f"Config file {self.config_path} not found.")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding the config file {self.config_path}.")
            raise

    def get_addresses(self): return self.config.get("transmitter")
    def get_mongo_url(self): return self.config.get("mongo_uri")
    def get_database_name(self): return self.config.get("database_name")
    def get_collection_name(self): return self.config.get("collection_name")
    def get_api_url(self): return self.config.get("api_url")
    def get_id_building(self): return self.config.get("id_building")
    def get_log_file(self): return self.config.get("log_file")
