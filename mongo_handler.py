from pymongo import MongoClient
import requests
import spinner_utils  # Import utility module
from config_singleton import get_config
from requests.exceptions import RequestException, ConnectionError
class MongoHandler:
    def __init__(self ):
        config = get_config()
        self.client = MongoClient(config.get_mongo_url())
        self.db = self.client[config.get_database_name()]
        self.collection = self.db[config.get_collection_name()]
        self.api_url = config.get_api_url()
        self.building_id = config.get_id_building()
        self.log_file = config.get_log_file()

    def find_user_by_code(self, code):
        """Finds a user by their code in MongoDB."""
        return self.collection.find_one({"user_code": code})
    
    def check_user_permissions(self,user, door):
        """Verifica si el usuario tiene acceso a la puerta indicada."""
        if not user.get("allowed", False):
            spinner_utils.print_error("Access Denied! User is disabled.")
            return False

        if door not in user.get("door_access", []):
            spinner_utils.print_error(f"Access Denied! User doesn't have access to door {door}.")
            return False

        return True
    def sync_users(self):
        """Fetches users from API and updates MongoDB."""
        try:
            response = requests.get(f"{self.api_url}/sync", params={"idBuilding": self.building_id}, timeout=5)
            response.raise_for_status()

            lstUsers = response.json()
            if not isinstance(lstUsers, list):
                print("Invalid response format.")
                return False
            
            self.collection.delete_many({"building_id": self.building_id})

            users_to_insert = [
                {
                    "building_id": self.building_id,
                    "user_code": user["user_code"],
                    "door_access": user["door_access"],
                    "allowed": user["allowed"]
                }
                for user in lstUsers
            ]

            self.collection.insert_many(users_to_insert)

            # ✅ Sync success message
            spinner_utils.print_success("Database synchronized successfully!")
            
            return True

        except (ConnectionError, RequestException) as e:
            # Capturar errores relacionados con la conexión a internet
            print(f"Network error occurred: {e}. Synchronization skipped.")
            return False

        except Exception as e:
            # Capturar cualquier otro error inesperado
            print(f"An error occurred during synchronization: {e}")
            return False

    def send_file_to_server(self):
        """Sends a file to a server using a POST request."""
        try:
            # Open the file in binary mode and send it with the 'files' parameter
            with open(self.log_file, 'rb') as file:
                files = {'file': (self.log_file, file, 'text/plain')}  # 'text/plain' es solo un ejemplo, usa el MIME type adecuado.
                response = requests.post(f"{self.api_url}/upload", files=files)
            
            if response.status_code == 200:
                print("File sent successfully!")
            else:
                print(f"Failed to send file. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
