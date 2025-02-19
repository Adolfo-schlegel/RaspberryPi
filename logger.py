import logging
from config_singleton import get_config
from datetime import datetime



# Configure logging using the file location from config
def configure_logging():
    config = get_config()
    log_file = config.get_log_file() # Default to 'access_log.txt' if not found

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )

def log_access(user_code, access_granted, door, user=None):
    """Logs user access attempts to the log file."""
    
    if user:  # Si el usuario existe
        print(f"User found: {user_code} - {user}")
        if not user.get("allowed", False):  # Verificar si está habilitado
            status = "Denied (User Disabled)"
        elif door not in user.get("door_access", []):  # Verificar acceso a la puerta
            status = "Denied (No Access to Door)"
        else:
            status = "Granted" if access_granted else "Denied"
    else:
        print(f"User not found: {user_code}")
        status = "Denied (User Not Found)"
    
    logging.info(f"User {user_code} - Access {status} - Door {door}")

##def log_access(user_code, access_granted, door):
##    """Registra el intento de acceso del usuario."""
##    status = "Granted" if access_granted else "Denied"
##    logging.info(f"User {user_code} - Access {status} - Door {door}")