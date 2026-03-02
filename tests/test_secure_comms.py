import unittest
from src.Telemetry_Parser import TelemetryParser

class TestSecureComms(unittest.TestCase):
    
    def setUp(self):
        self.parser = TelemetryParser()

    def test_telemetry_fields(self):
        """Verify that parsed telemetry contains all critical mission keys."""
        # Using generate_data to check fields
        data = self.parser.generate_data()
        required_keys = ["timestamp", "altitude", "battery", "status", "lat", "lon"]
        
        for key in required_keys:
            self.assertIn(key, data)

    def test_secure_packet_format(self):
        """Verify the structure of the prepared secure packet."""
        packet = self.parser.prepare_packet()
        self.assertIn("payload", packet)
        self.assertIn("signature", packet)
        self.assertIn("metadata", packet)
        self.assertEqual(packet["metadata"]["encryption"], "AES-256-GCM")

if __name__ == '__main__':
    unittest.main()
