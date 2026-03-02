import time
import sys
import random
import threading
try:
    from colorama import Fore, Back, Style, init
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
except ImportError:
    print("Please run: pip install -r requirements_secure.txt")
    sys.exit(1)

from src.OBC_Main import OnBoardComputer
from src.Telemetry_Parser import TelemetryParser

# Initialize Colorama
init(autoreset=True)
console = Console()

def print_banner():
    banner = f"""
    {Fore.GREEN}
    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗
    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
    ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  
    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  
    ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗
    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    {Fore.CYAN}    >>> TEKNOFEST GUVENLI UYDU SIMULATOR V1.0 <<<
    {Fore.RED}    >>> CLASSIFIED: TOP SECRET // AES-256 <<<
    """
    print(banner)

def generate_telemetry_table(data):
    table = Table(title="SATELLITE TELEMETRY LIVE ESTABLISHED")
    table.add_column("METRIC", justify="right", style="cyan", no_wrap=True)
    table.add_column("VALUE", style="magenta")

    for key, value in data.items():
        table.add_row(key.upper(), str(value))
    
    return table

# Shared memory for inter-satellite awareness (Simulation of Inter-Satellite Link)
global_swarm_context = {}
context_lock = threading.Lock()

def run_satellite_node(sat_id, gs_url):
    """
    Runs a single satellite node in a thread.
    """
    satellite = OnBoardComputer(satellite_id=sat_id)
    print(f"{Fore.CYAN}[SYSTEM] {sat_id} Link establishing...")
    
    try:
        while True:
            # Get peer data from global context
            with context_lock:
                peers = global_swarm_context.copy()
            
            # Run cycle with peer awareness
            packet = satellite.run_cycle(peer_telemetry=peers)
            
            # Decrypt locally for GS simulation
            raw_data = satellite.parser.generate_data()
            
            # Update global context
            with context_lock:
                global_swarm_context[sat_id] = {
                    "satellite_id": sat_id,
                    "threat_level": packet.get("threat_level", 0),
                    "pos": (raw_data['lat'], raw_data['lon'])
                }

            # Post to Global Swarm GS
            try:
                requests.post(gs_url, json={
                    "satellite_id": sat_id,
                    "payload": packet.get("payload", ""),
                    "signature": packet.get("signature", ""),
                    "metadata": packet.get("metadata", {}),
                    "threat_level": packet.get("threat_level", 0),
                    "threat_status": packet.get("threat_status", "SECURE"),
                    "decrypted": raw_data
                }, timeout=0.2)
            except:
                pass
            
            time.sleep(1 + random.uniform(0, 0.5))
    except Exception as e:
        print(f"{Fore.RED}[{sat_id}] CRITICAL_FAILURE: {e}")

def simulation_loop():
    gs_url = "http://localhost:5000/api/telemetry"
    
    sat_ids = ["SAT-ALPHA", "SAT-BRAVO", "SAT-CHARLIE"]
    threads = []
    
    print(f"{Fore.GREEN}[SWARM] INITIALIZING {len(sat_ids)} SECURE NODES...")
    
    for s_id in sat_ids:
        t = threading.Thread(target=run_satellite_node, args=(s_id, gs_url), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.5)

    print(f"{Fore.YELLOW}[SWARM] ALL NODES OPERATIONAL. VIEWING LIVE AT GS: {gs_url}")
    
    try:
        # Just keep main thread alive or show global summary
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[SYSTEM] SWARM DEACTIVATED BY COMMANDER.")

if __name__ == "__main__":
    print_banner()
    if "--mode=simulation" in sys.argv:
        simulation_loop()
    else:
        print(f"{Fore.WHITE}Usage: python mission_control.py --mode=simulation")
