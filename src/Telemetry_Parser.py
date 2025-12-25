import json
import time
import random

class TelemetryParser:
    """
    Parses incoming hex data from the satellite and formats it for the Ground Station.
    """
    
    @staticmethod
    def parse_packet(hex_data):
        """
        Simulates parsing a raw hex packet into a readable dictionary.
        """
        # Simulation: In a real scenario, this would bit-shift incoming bytes.
        # Here we pretend to decode a secure payload.
        
        try:
            # Mock decoding process
            return {
                "timestamp": time.strftime("%H:%M:%S"),
                "battery_voltage": round(random.uniform(11.5, 12.6), 2),
                "internal_temp": round(random.uniform(35.0, 45.0), 1),
                "gps_lat": 40.990 + random.uniform(-0.001, 0.001),
                "gps_lon": 40.230 + random.uniform(-0.001, 0.001),
                "status": "NORMAL",
                "uplink_quality": f"{random.randint(90, 100)}%"
            }
        except Exception as e:
            return {"error": "PACKET_CORRUPTION_DETECTED", "details": str(e)}

    @staticmethod
    def encrypt_command(command):
        """
        Wraps a command in a mock specific header for transmission.
        """
        return f"SECURE_CMD::[ {command} ]::END"
