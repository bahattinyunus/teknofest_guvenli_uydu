import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .PQC_Engine import PQCKyberEngine

class SecureCryptoEngine:
    """
    Simulation of a high-performance Hybrid AES-256-GCM + CRYSTALS-Kyber engine.
    """
    
    def __init__(self, key: bytes = None):
        self.key = key or os.urandom(32)
        self.aesgcm = AESGCM(self.key)
        self.hmac_key = os.urandom(32)
        self.pqc = PQCKyberEngine()
        self.pqc_enabled = True

    def encrypt_telemetry(self, data: bytes) -> bytes:
        """
        Encrypts telemetry data using Hybrid Mode.
        Returns: PQC_Header + Nonce + Ciphertext
        """
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, data, None)
        
        if self.pqc_enabled:
            # Simulate PQC Encapsulation of the session key/metadata
            _, pqc_blob = self.pqc.encapsulate(self.pqc.public_key)
            return b"PQC_V1" + pqc_blob + nonce + ciphertext
            
        return nonce + ciphertext

    def decrypt_command(self, encrypted_command: bytes) -> bytes:
        """
        Decrypts incoming command. Handles Hybrid PQC or Legacy AES.
        """
        try:
            if encrypted_command.startswith(b"PQC_V1"):
                # Strip PQC header and blob (Simulation: 6 bytes header + 32 bytes blob)
                pqc_blob = encrypted_command[6:38]
                payload = encrypted_command[38:]
                
                # Decapsulate (Simplified)
                self.pqc.decapsulate(pqc_blob, self.pqc.private_key)
                
                nonce = payload[:12]
                ciphertext = payload[12:]
            else:
                nonce = encrypted_command[:12]
                ciphertext = encrypted_command[12:]
                
            return self.aesgcm.decrypt(nonce, ciphertext, None)
        except Exception as e:
            print(f"[SECURITY] Decryption failed (Hybrid/Legacy): {e}")
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
