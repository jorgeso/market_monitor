from market_monitor.services.orchestrator import start_monitoring_market
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    start_monitoring_market()