import unittest
import os
from src.Crypto_Engine import SecureCryptoEngine

class TestCryptoEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = SecureCryptoEngine()

    def test_encryption_decryption(self):
        """Verify that data can be encrypted and decrypted correctly."""
        original_data = b"MISSION_DATA_77"
        encrypted = self.engine.encrypt_telemetry(original_data)
        
        # Ensure it's actually different
        self.assertNotEqual(original_data, encrypted)
        
        decrypted = self.engine.decrypt_command(encrypted)
        self.assertEqual(original_data, decrypted)

    def test_integrity_signature(self):
        """Verify HMAC signature generation and verification."""
        message = b"TELEMETRY_PACKET_001"
        signature = self.engine.sign_message(message)
        
        # Verify valid signature
        self.assertTrue(self.engine.verify_signature(message, signature))
        
        # Verify invalid signature for modified message
        self.assertFalse(self.engine.verify_signature(message + b"modified", signature))

    def test_decryption_failure(self):
        """Verify that decryption returns None on corrupted data."""
        encrypted = self.engine.encrypt_telemetry(b"SECRET")
        corrupted = bytearray(encrypted)
        # Corrupt the last byte (guaranteed to be in the ciphertext/tag)
        corrupted[-1] ^= 0xFF 
        
        decrypted = self.engine.decrypt_command(bytes(corrupted))
        self.assertIsNone(decrypted)

if __name__ == '__main__':
    unittest.main()
