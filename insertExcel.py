import openpyxl
import os
from dotenv import load_dotenv

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