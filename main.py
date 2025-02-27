from rf24_handler import RF24Handler
from mongo_handler import MongoHandler
import threading
import time
import spinner_utils 
import logger

# Initialize handlers
rf24 = RF24Handler()
mongo = MongoHandler()

def sync_periodically(interval=600):
    """Automatically sync users every 'interval' seconds."""
    while True:
        mongo.sync_users()
        mongo.send_file_to_server()
        time.sleep(interval)

# Start sync thread (every 10 minutes)
sync_thread = threading.Thread(target=sync_periodically, daemon=True)
sync_thread.start()
logger.configure_logging()

print(spinner_utils.MAGENTA + "🚀 Starting..." + spinner_utils.RESET)
spinner_utils.print_kawaii_smiling_face()
spinner_utils.colorful_spinner(3)

while True:
    received_code, door = rf24.read_code()

    if received_code:
        if len(received_code) % 2 != 0:
            print(f"Invalid code length: {received_code}")
            continue
               
        try:
            user = mongo.find_user_by_code(received_code)  
            
            if user:
                # Verificación de permisos
                if not user.get("allowed", False) or door not in user.get("door_access", []):
                    access_granted = False
                    spinner_utils.print_error("Access Denied!")
                else:
                    access_granted = True
                    spinner_utils.print_success("Access Granted!")
            else:
                access_granted = False
                spinner_utils.print_error("Access Denied!")
            
            logger.log_access(received_code, access_granted, door, user)
        except KeyError as e:
            spinner_utils.print_error(f"Error processing code: Missing key {e}")
        except Exception as e:
            spinner_utils.print_error(f"Error processing code: {e}")
    
    rf24.wait()


