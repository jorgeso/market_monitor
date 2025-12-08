from market_monitor.services.orchestrator import perform_market_check
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    perform_market_check()