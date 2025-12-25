import unittest
from src.Telemetry_Parser import TelemetryParser

class TestSecureComms(unittest.TestCase):
    
    def test_telemetry_fields(self):
        """Verify that parsed telemetry contains all critical mission keys."""
        data = TelemetryParser.parse_packet(b"RAW_HEX")
        required_keys = ["timestamp", "battery_voltage", "status", "uplink_quality"]
        
        for key in required_keys:
            self.assertIn(key, data)

    def test_command_encryption_format(self):
        """Verify command wrapper format."""
        cmd = "FIRE_THRUSTERS"
        encrypted = TelemetryParser.encrypt_command(cmd)
        self.assertTrue(encrypted.startswith("SECURE_CMD::"))
        self.assertTrue(encrypted.endswith("::END"))
        self.assertIn(cmd, encrypted)

if __name__ == '__main__':
    unittest.main()
