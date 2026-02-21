import requests
from dotenv import load_dotenv
import os

load_dotenv()
get_api_key = os.getenv("NINJA_API_KEY")
get_api_domain = os.getenv("NINJA_API_DOMAIN")

print(f"API Domain: {get_api_domain}")

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
        return data
    else:
        print(f"Error fetching Bitcoin price: {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
def main():
    bitcoin_price = get_bitcoin_price()
    if bitcoin_price is not None:
        # maybe change bitcoin price from usd to hkd for my own transaction
        print(f"Current Bitcoin price in USD: {bitcoin_price}")
    else:
        print("Failed to retrieve Bitcoin price.")

    # In the future, insert the logic to place order through Hashkey API here.
    # For the logic to place order (for example when I sell and when I buy), I will set up a simple rule-based system.

if __name__ == "__main__":
    main()