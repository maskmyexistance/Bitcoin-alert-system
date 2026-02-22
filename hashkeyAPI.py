import requests
from dotenv import load_dotenv
import os
import twilio
import json
import hmac
import hashlib
from connectPushNoti import test_notifier
from insertExcel import insert_record_to_excel
import logging
from logger import configure_logger

def test_hashkey_api():
    pass

def get_credentials() -> dict:

    load_dotenv()
    credentials = {}
    credentials["api_key"] = os.getenv("HASHKEY_API_KEY")
    credentials["api_secret"] = os.getenv("HASHKEY_API_SECRET")
    credentials["base_url"] = os.getenv("HASHKEY_API_DOMAIN_DEV")
    #credentials["base_url"] = os.getenv("HASHKEY_API_DOMAIN_PROD")

    credentials["headers"] = {
        'X-HK-APIKEY': credentials["api_key"]
    }

    return credentials

def create_signature(self, content):
        """
        Create HMAC signature for authentication.

        Args:
            content (str): The content to be signed.

        Returns:
            str: The HMAC signature.
        """
        content_bytes = content.encode('utf-8')
        hmac_digest = hmac.new(
            self.user_secret.encode('utf-8'),
            content_bytes,
            hashlib.sha256
        ).hexdigest()
        return hmac_digest

def place_order(symbol, side, order_type, price, quantity, timestamp):
    configure_logger()
    logger = logging.getLogger(__name__)
    cred = get_credentials()
    url = f"{cred['base_url']}/v1/orders"
    headers = cred['headers']

    # Need to understand what these 6 field means
    data = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp
        }
    
    response = requests.post(
        # the url is right now is in testing environement
        url,
        headers=headers,
        data=data
    )

    if response.status_code == 200:
        data = response.json()
        logger.info("Response:")
        logger.info(json.dumps(data, indent=4))

        # Insert transaction record to excel
        excel = insert_record_to_excel(side, price, quantity)

        if excel is not None:
           logger.info("Record inserted to Excel successfully.")

        # Apart from insert transaction to excel, send push notification also.
        response = test_notifier('bark', f'Bitcoin Transaction Recorded:', f'Buy or Sell: {side} \nPrice: {price}, \nQuantity: {quantity}, \nVolume: {price*quantity}')
        response_json = response.json()
        if response_json.get("code") == 200:
            logger.info("Push notification sent successfully.")
        else:     
            logger.info(f"Failed to send push notification. \nResponse code: {response_json['code']}, \nResponse text: {response_json['message']}")

        return data

    else:
        try:
            error_json = response.json()
            logger.info("Error:")
            logger.info(json.dumps(error_json, indent=4))  # log formatted error response
        except json.JSONDecodeError:
            logger.info(f"Error: {response.status_code} - {response.text}")
        return None