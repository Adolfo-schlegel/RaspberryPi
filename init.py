from pyrf24 import RF24, RF24_1MBPS, RF24_PA_LOW
from pymongo import MongoClient
import json
import time

# Load MongoDB config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

MONGO_URI = config["mongo_uri"]
DB_NAME = config["database_name"]
COLLECTION_NAME = config["collection_name"]

radio = RF24(22, 0)

if not radio.begin():
    print("NRF24L01 no detectado")
    exit()

# Radio Config
radio.setDataRate(RF24_1MBPS)
radio.setPALevel(RF24_PA_LOW)
radio.openReadingPipe(1, b"1Node")
radio.startListening()

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]
print("Esperando mensajes...")

while True:
    if radio.available():
        buffer = radio.read(32)
        
        buffer = buffer.rstrip(b'\x00')
        
        received_code = buffer.decode("utf-8", errors="ignore").strip()

        received_code = received_code.replace(" ", "").strip()

        if len(received_code) % 2 != 0:
            print(f"Invalid code length: {received_code}")
            continue
        
        try:
            user = users_collection.find_one({"code": received_code})

            if user:
                print(f"Access granted: {user['name']}")
            else:
                print("Access denied: Unknown code")
        except Exception as e:
            print(f"Error processing code: {e}")
    time.sleep(0.1)
