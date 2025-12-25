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

def simulation_loop():
    satellite = OnBoardComputer()
    
    print(f"{Fore.YELLOW}[SYSTEM] Establishing Secure Link...", end="\r")
    time.sleep(2)
    print(f"{Fore.GREEN}[SYSTEM] LINK ESTABLISHED. HANDSHAKE VERIFIED.")
    time.sleep(1)

    with Live(generate_telemetry_table({}), refresh_per_second=4) as live:
        try:
            while True:
                data = satellite.run_cycle()
                
                if "type" in data and data["type"] == "ALERT":
                    console.print(f"[bold red]!!! ALERT: {data['msg']} !!![/bold red]")
                    time.sleep(1)
                else:
                    live.update(generate_telemetry_table(data))
                
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[SYSTEM] LINK TERMINATED BY USER.")

if __name__ == "__main__":
    print_banner()
    if "--mode=simulation" in sys.argv:
        simulation_loop()
    else:
        print(f"{Fore.WHITE}Usage: python mission_control.py --mode=simulation")
