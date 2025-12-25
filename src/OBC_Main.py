import time
import random
from .Telemetry_Parser import TelemetryParser

class OnBoardComputer:
    """
    The main brain of the satellite. Manages state, sensors, and secure comms.
    """
    
    def __init__(self):
        self.state = "BOOT"
        self.system_integrity = 100
        print("[OBC] System Initializing...")
        time.sleep(1)
        self.state = "IDLE"

    def read_sensors(self):
        """
        Simulates reading data from I2C sensors.
        """
        return {
            "gyro": (0.01, -0.02, 0.05),
            "temp": 42.0,
            "power_bus": 12.4
        }

    def encrypt_and_transmit(self):
        """
        Packages sensor data and pretends to send it via LoRa.
        """
        raw_data = self.read_sensors()
        # In a real system, C++ bindings to Crypto_Engine would be called here.
        packet = TelemetryParser.parse_packet(raw_data) 
        
        # Simulate transmission delay
        time.sleep(0.5)
        return packet

    def run_cycle(self):
        """
        Single cycle of the main loop.
        """
        if random.random() < 0.05:
            # Simulate a rare anomaly
            return {"type": "ALERT", "msg": "HIGH RADIATION DETECTED"}
        
        return self.encrypt_and_transmit()
