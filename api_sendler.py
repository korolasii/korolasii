import xmltodict
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import os
import time
from pprint import pprint
from dotenv import load_dotenv


_last_ref_sent_date = "2025-07-23"

def openFile(name) -> str:
    with open(name, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    return xml_content


def main_for_ref(name) -> dict:
    data_dict = xmltodict.parse(openFile(name))

    desired_fields = ['Code', 'Name', 'Producer', 'Tax', 'Price', 'Quantity', 'PriceReserve', 'Barcode']

    offers = data_dict.get('Offers', {}).get('Offer', [])

    if not isinstance(offers, list):
        offers = [offers]

    result_offers = []

    for item in offers:
        if item is None or not isinstance(item, dict):
            continue

        offer_data = {
            key: item.get(f"@{key}")
            for key in desired_fields
            if f"@{key}" in item
        }

        code = item.get('@Code')

        if code:
            offer_data['SupplierCodes'] = [
                {
                    "ID": "Barcode",
                    "Code": code
                }
            ]

        result_offers.append(offer_data)

    result = {
        "Offers": result_offers,
        "Suppliers": [
            {
                "ID": "Barcode",
                "Name": "Barcode",
                "Edrpo": "Barcode"
            }
        ]
    }

    return result




def main_for_rests(branch_code="30547", name = "output.xml"):
    now = (datetime.now()).strftime("%d.%m.%Y %H:%M:%S")

    data = xmltodict.parse(openFile(name))
    offers = data.get('Offers', {}).get('Offer', [])

    rests = []

    for item in offers:
        if item is None or not isinstance(item, dict):
            continue
        try:
            rest_item = {
                "Code": item.get('@Code', ''),
                "Price": float(item.get('@Price', 0)),
                "PriceReserve": float(item.get('@PriceReserve', 0)),
                "Qty": float(item.get('@Quantity', 0)),
            }
            rests.append(rest_item)
        except Exception as e:
            print(f"Ошибка при обработке товара: {item}, ошибка: {e}")

    result = {
        "Branches": [
            {
                "Code": branch_code,
                "Rests": rests,
                "DateTime": now
            }
        ]
    }

    return result



def send_to_api(data, url, headers={'Content-Type': 'application/json'}):
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(os.getenv('NAME'), os.getenv('PASSWORD'))) # for work
    # response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth("310", "41cfc799ba75")) # for test
    print(data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text}")
    return response


def main(name):
    print(name)
    load_dotenv()
    current_date = datetime.now().date()
    global _last_ref_sent_date
    if "люстдорфська" in name.lower():
        print("Люстдорфська")
        result = main_for_rests("55935 ", name) # for work
        send_to_api(result, "https://import.tabletki.ua/Import/Rests") # for work
    elif "троїцька" in name.lower():
        result = main_for_rests("58767 ", name) # for work
        send_to_api(result, "https://import.tabletki.ua/Import/Rests") # for work
        
    if _last_ref_sent_date != current_date:
        print("\nОтправка справочных данных (Ref) за сегодня...")
        result_ref = main_for_ref(name) 
        send_to_api(result_ref, " https://import.tabletki.ua/Import/Ref/55935") # for work
        

        _last_ref_sent_date = current_date 
        print("Справочные данные (Ref) успешно отправлены и отмечены.")



# def main(name):
#     load_dotenv()
#     if "Люстдорфська" in name:
#         if (datetime.now() + timedelta(hours=3)).hour >= 20:
#             result_ref = main_for_ref(name) 
#             send_to_api(result_ref, " https://testenv-import.tabletki.ua/Import/Ref/30547") # for test

#         result = main_for_rests("30547 ", name) # for test
#         send_to_api(result, "https://testenv-import.tabletki.ua/Import/Rests") # for test
#     elif "Троїцька" in name:
#         if (datetime.now() + timedelta(hours=3)).hour >= 20:
#             result_ref = main_for_ref(name)

#             send_to_api(result_ref, " https://testenv-import.tabletki.ua/Import/Ref/30548") # for test

#         result = main_for_rests("30548 ", name) # for test
#         send_to_api(result, "https://testenv-import.tabletki.ua/Import/Rests") # for test
if __name__ == "__main__":
    main("Люстдорфська.xml")
    main("Троїцька.xml")
