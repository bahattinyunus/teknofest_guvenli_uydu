import json
import time
import random

import json
import time
import math
import random
from .Crypto_Engine import SecureCryptoEngine

class TelemetryParser:
    """
    Simulates a satellite's telemetry sub-system.
    Generates realistic orbital data and handles secure encapsulation.
    """
    
    def __init__(self):
        self.crypto = SecureCryptoEngine()
        self.start_time = time.time()
        self.base_lat = 41.0082  # Teknofest location (approx)
        self.base_lon = 28.9784
        self.altitude = 500.0  # meters
        self.battery = 100.0
        
    def generate_data(self):
        """
        Generates realistic satellite telemetry.
        """
        elapsed = time.time() - self.start_time
        
        # Simulated orbital motion (simple sine waves for attitude)
        pitch = 5.0 * math.sin(elapsed * 0.5) + random.uniform(-0.5, 0.5)
        roll = 3.0 * math.cos(elapsed * 0.3) + random.uniform(-0.5, 0.5)
        yaw = (elapsed * 2.0) % 360.0
        
        # Battery decay
        self.battery -= 0.01
        if self.battery < 0: self.battery = 0
        
        # GPS Walk
        self.base_lat += random.uniform(-0.0001, 0.0001)
        self.base_lon += random.uniform(-0.0001, 0.0001)
        
        data = {
            "timestamp": time.time(),
            "altitude": round(self.altitude + 10 * math.sin(elapsed * 0.1), 2),
            "pitch": round(pitch, 2),
            "roll": round(roll, 2),
            "yaw": round(yaw, 2),
            "battery": round(self.battery, 2),
            "lat": round(self.base_lat, 6),
            "lon": round(self.base_lon, 6),
            "status": "NOMINAL" if self.battery > 20 else "LOW_BATTERY"
        }
        return data

    def prepare_packet(self):
        """
        Encapsulates, encrypts, and signs a telemetry packet.
        """
        raw_data = self.generate_data()
        json_data = json.dumps(raw_data).encode()
        
        # Encrypt
        encrypted = self.crypto.encrypt_telemetry(json_data)
        
        # Sign (Integrity)
        signature = self.crypto.sign_message(encrypted)
        
        return {
            "payload": encrypted.hex(),
            "signature": signature.hex(),
            "metadata": {
                "version": "1.2.0-secure",
                "encryption": "AES-256-GCM",
                "integrity": "HMAC-SHA256"
            }
        }

    def parse_packet(self, packet_hex):
        """
        For Ground Station use: parses the secure packet back to JSON.
        """
        # In this simulation, we'll assume the GS has the same derived keys.
        # This function would be used by the GS backend.
        return json.loads(packet_hex) # Placeholder for actual decryption logic in GS
