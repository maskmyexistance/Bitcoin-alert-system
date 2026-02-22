import logging
from logger import configure_logger
import requests
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
logger = logging.getLogger()
configure_logger(log_path=os.getenv("ROOT_PATH") + f"\\Log\\bitcoin_price_monitoring_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log")
logger.info("Starting Bitcoin price monitoring system...")
get_api_key = os.getenv("NINJA_API_KEY")
get_api_domain = os.getenv("NINJA_API_DOMAIN")

# in the future, I will add a monitoring system such as Datadog or Prometheus to track changes in the Bitcoin price. Then set up alerts to notify me if significant price change occur.
# search later how to use python to interact with Datadog or Promethus API

def get_bitcoin_price():
    url = f"{get_api_domain}/v1/bitcoin"
    headers = {
        "X-Api-Key": get_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Successfully retrieved Bitcoin price.")
        logger.info(f"Response data: {str(json.dumps(data, indent=4))}")
        return data
    else:
        logger.info(f"Error fetching Bitcoin price: {response.status_code}")
        logger.info(f"Response: {response.text}")
        return None
    
def main():
    bitcoin_price = get_bitcoin_price()
    # insert bitcoin price into json files
    if bitcoin_price is not None:       
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        logger.info(f"Saving Bitcoin price data to JSON file: bitcoin_price_{timestamp}.json")
        try:
            with open(f"{os.getenv('ROOT_PATH')}\\Staging\\bitcoin_price_{timestamp}.json", "w") as f:
                json.dump(bitcoin_price, f, indent=4)
            logger.info("Successfully saved Bitcoin price data to JSON file.")
        except Exception as e:
            logger.info(f"Error saving Bitcoin price data to JSON file: {str(e)}")
    else:
        logger.info("Failed to retrieve Bitcoin price.")

    # In the future, insert the logic to place order through Hashkey API here.
    # For the logic to place order (for example when I sell and when I buy), I will set up a simple rule-based system.

if __name__ == "__main__":
    main()