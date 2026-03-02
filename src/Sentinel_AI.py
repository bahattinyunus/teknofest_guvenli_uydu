import time

class SentinelAI:
    """
    AI-Sentinel: Anomaly detection and cyber-security monitor.
    Analyzes telemetry patterns and command integrity in real-time.
    """
    
    def __init__(self):
        self.last_command_time = 0
        self.command_history = []
        self.threat_score = 0.0
        self.last_alt = None

    def analyze_telemetry(self, data):
        """
        Detects physical anomalies in sensor data.
        Returns: threat_increment (float)
        """
        inc = 0.0
        
        # 1. Altitude Jump Detection
        if self.last_alt is not None:
            diff = abs(data['altitude'] - self.last_alt)
            if diff > 50: # Impossible 50m jump in 1s
                inc += 25.0
                print(f"[SENTINEL] ANOMALY: ALTITUDE_JUMP DETECTED ({diff}m)")
        
        self.last_alt = data['altitude']
        
        # 2. Battery Surge Detection
        if data['battery'] > 100 or data['battery'] < 0:
            inc += 15.0
            print("[SENTINEL] ANOMALY: BATTERY_LEVEL_OUT_OF_BOUNDS")

        return inc

    def analyze_command(self, cmd_text):
        """
        Detects suspicious command patterns (e.g., DoS, Brute Force).
        """
        now = time.time()
        inc = 0.0
        
        # 1. Frequency Analysis (Flood Protection)
        if now - self.last_command_time < 0.2: # Max 5 cmds/sec
            inc += 20.0
            print("[SENTINEL] SECURITY_THREAT: COMMAND_FLOODING DETECTED")
        
        # 2. Critical System Tampering Attempt
        critical_keywords = ["KILL_SWITCH", "FORMAT_SD", "SHUTDOWN"]
        if any(kw in cmd_text.upper() for kw in critical_keywords):
            inc += 50.0 # High risk
            print(f"[SENTINEL] SECURITY_ALERT: ATTEMPTED ACCESS TO CRITICAL_CMD: {cmd_text}")

        self.last_command_time = now
        return inc

    def update_threat_level(self, increment):
        """
        Updates the global threat score and applies decay over time.
        """
        self.threat_score = min(100.0, self.threat_score + increment)
        
        # Natural decay: 2 points per cycle if no new threats
        if increment == 0:
            self.threat_score = max(0.0, self.threat_score - 2.0)
            
        return round(self.threat_score, 1)

    def get_status(self):
        if self.threat_score < 20: return "SECURE"
        if self.threat_score < 60: return "WARNING"
        return "CRITICAL_THREAT"
