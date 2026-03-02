import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureCryptoEngine:
    """
    Simulation of a high-performance AES-256-GCM and HMAC-SHA256 engine.
    In a real STM32 system, these would be hardware accelerated.
    """
    
    def __init__(self, key: bytes = None):
        # In a real mission, this key would be pre-shared or derived via ECDH.
        self.key = key or os.urandom(32) # 256-bit key
        self.aesgcm = AESGCM(self.key)
        self.hmac_key = os.urandom(32)

    def encrypt_telemetry(self, data: bytes) -> bytes:
        """
        Encrypts telemetry data using AES-GCM.
        Returns: Nonce (12 bytes) + Ciphertext + Tag (16 bytes)
        """
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, data, None)
        return nonce + ciphertext

    def decrypt_command(self, encrypted_command: bytes) -> bytes:
        """
        Decrypts incoming command using AES-GCM.
        Expects: Nonce (12 bytes) + Ciphertext + Tag
        """
        try:
            nonce = encrypted_command[:12]
            ciphertext = encrypted_command[12:]
            return self.aesgcm.decrypt(nonce, ciphertext, None)
        except Exception as e:
            print(f"[SECURITY] Decryption failed: {e}")
            return None

    def sign_message(self, message: bytes) -> bytes:
        """
        Generates an HMAC-SHA256 signature for telemetry integrity.
        """
        h = hmac.new(self.hmac_key, message, hashlib.sha256)
        return h.digest()

    def verify_signature(self, message: bytes, signature: bytes) -> bool:
        """
        Verifies HMAC signature for incoming commands.
        """
        h = hmac.new(self.hmac_key, message, hashlib.sha256)
        return hmac.compare_digest(h.digest(), signature)
