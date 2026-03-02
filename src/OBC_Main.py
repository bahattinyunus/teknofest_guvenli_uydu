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
        self.parser = TelemetryParser()
        print("[OBC] System Initializing...")
        time.sleep(1)
        self.state = "IDLE"

    def process_command(self, secure_packet):
        """
        Decrypts and executes an incoming command packet.
        """
        # In this simulation, we assume the command is already hex-encoded payload
        decrypted = self.parser.crypto.decrypt_command(bytes.fromhex(secure_packet))
        if decrypted:
            cmd = decrypted.decode()
            print(f"[OBC] EXECUTING SECURE COMMAND: {cmd}")
            return True
        return False

    def run_cycle(self):
        """
        Single cycle of the main loop.
        """
        if random.random() < 0.05:
            # Simulate a rare anomaly
            return {"type": "ALERT", "msg": "HIGH RADIATION DETECTED"}
        
        # Prepare secure telemetry packet
        return self.parser.prepare_packet()
