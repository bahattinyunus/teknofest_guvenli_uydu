import time
import random
from .Sentinel_AI import SentinelAI

class OnBoardComputer:
    """
    The main brain of the satellite. Manages state, sensors, and secure comms.
    """
    
    def __init__(self, satellite_id="SAT_ALPHA"):
        self.id = satellite_id
        self.state = "BOOT"
        self.system_integrity = 100
        self.parser = TelemetryParser()
        self.sentinel = SentinelAI()
        print(f"[OBC:{self.id}] System Initializing...")
        time.sleep(1)
        self.state = "IDLE"

    def process_command(self, secure_packet):
        """
        Decrypts and executes an incoming command packet.
        """
        # Sentinel Check 1: Rate & Content
        # In a real system, we'd check BEFORE decrypting if possible (HMAC fail), 
        # but here we decrypt first to check content.
        decrypted = self.parser.crypto.decrypt_command(bytes.fromhex(secure_packet))
        
        if decrypted:
            cmd = decrypted.decode()
            threat_inc = self.sentinel.analyze_command(cmd)
            self.sentinel.update_threat_level(threat_inc)
            
            if self.sentinel.threat_score > 80:
                print(f"[OBC:{self.id}] SECURITY_LOCKOUT: COMMAND IGNORED DUE TO HIGH THREAT.")
                return False
                
            print(f"[OBC:{self.id}] EXECUTING SECURE COMMAND: {cmd}")
            return True
        return False

    def swarm_sync(self, peer_data):
        """
        Simulates state synchronization with other satellites in the swarm.
        Verifies peer health and updates local world-state.
        """
        peer_id = peer_data.get("satellite_id")
        peer_threat = peer_data.get("threat_level", 0)
        
        if peer_threat > 50:
            print(f"[OBC:{self.id}] WARNING: Peer {peer_id} exhibits SUSPICIOUS BEHAVIOR (Threat: {peer_threat})")
            # In a real swarm, we might isolate the node here.
            
        return True

    def run_cycle(self, peer_telemetry=None):
        """
        Single cycle of the main loop.
        """
        # Sync with peers if available
        if peer_telemetry:
            for p_id, p_data in peer_telemetry.items():
                if p_id != self.id:
                    self.swarm_sync(p_data)

        # Generate telemetry
        raw_telemetry = self.parser.generate_data()
        
        # Sentinel Check 2: Physical Anomalies
        threat_inc = self.sentinel.analyze_telemetry(raw_telemetry)
        threat_level = self.sentinel.update_threat_level(threat_inc)
        
        # Prepare secure telemetry packet
        packet = self.parser.prepare_packet()
        packet["satellite_id"] = self.id
        packet["threat_level"] = threat_level
        packet["threat_status"] = self.sentinel.get_status()
        
        if random.random() < 0.05:
            # Simulate a rare anomaly
            return {"type": "ALERT", "msg": "HIGH RADIATION DETECTED", "satellite_id": self.id}
        
        return packet
