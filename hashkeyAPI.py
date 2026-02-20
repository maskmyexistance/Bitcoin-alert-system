import requests
from dotenv import load_dotenv
import os
import twilio
import json
import hmac
import hashlib
import openpyxl

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

def insert_record_to_excel(bors:str, price:float, quantity:float):

    # right now these price quality value are for testing, in prod these will be extracted from hashkey API response.
    load_dotenv()

    excel_path = os.getenv("BITCOIN_TRANSACTION_EXCEL_PATH")
    try:
        excel_file = openpyxl.load_workbook(excel_path)
    except FileNotFoundError:
        print("Excel file not found.")
        return None
    except PermissionError:
        print("Permission denied. Please close the Excel file if it's open and try again.")
        return None
    
    excel_sheet = excel_file.active
    # Extract first 4 columns of the first row as headers and print them
    header:list = [cell.value for cell in excel_sheet[1][:4]]
    print(f"Excel headers: {header}")

    # loop each row, find the first empty row, and insert data into the first 4 columns
    for row in excel_sheet.iter_rows(min_row=2, max_col=4):
        if all(cell.value is None for cell in row):
            print(f"""Inserting record into Excel: 
                  方向: {bors}, 
                  成交價: {price}, 
                  數量: {quantity}
                  交易量: {price*quantity}
""")
            row[0].value = bors  # 方向
            row[1].value = price  # 成交價 in HKD
            row[2].value = quantity  # 數量
            row[3].value = price*quantity  #交易量

            # Column 4 will be storing the handling fee, will add the logic later.
            break
    
    excel_file.save(excel_path)
    return excel_file

def place_order(symbol, side, order_type, price, quantity, timestamp):
    cred = get_credentials()
    url = f"{cred['base_url']}/v1/orders"
    headers = cred['headers']
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
        print("Response:")
        print(json.dumps(data, indent=4))
        # send SMS or email notification here if needed
        return data

    else:
        try:
            error_json = response.json()
            print("Error:")
            print(json.dumps(error_json, indent=4))  # Print formatted error response
        except json.JSONDecodeError:
            print(f"Error: {response.status_code} - {response.text}")
        return None