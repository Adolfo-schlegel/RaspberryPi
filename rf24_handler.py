from pyrf24 import RF24, RF24_1MBPS, RF24_PA_LOW
from config_singleton import get_config
import time

class RF24Handler:
    def __init__(self, ce_pin=22, csn_pin=0):
        self.radio = RF24(ce_pin, csn_pin)        

        if not self.radio.begin():
            raise RuntimeError("NRF24L01 not detected")
        
        config = get_config()
        self.addresses = config.get_addresses()   
        self.radio.setDataRate(RF24_1MBPS)
        self.radio.setPALevel(RF24_PA_LOW)        
        self.radio.openReadingPipe(1, self.addresses.encode('utf-8') )
        self.radio.startListening()
        self.radio.setChannel(80)

    def read_code(self):
        if self.radio.available():

            buffer = self.radio.read(32).rstrip(b'\x00')
            
            message = buffer.decode("utf-8", errors="ignore").strip().replace(" ", "")
          
            if ":" in message:
                door_name, uid = message.split(":")
                door_name = int(door_name)  
            return uid, door_name  
    
        return None, None


    def wait(self, seconds=0.1):
        time.sleep(seconds)
