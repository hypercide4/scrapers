import random
import time
from urllib.parse import unquote

import pandas as pd
from curl_cffi import requests

cookies = {}  # replace with curl cookies
headers = {}  # replace with curl headers


def safe_get(data, keys, default="N/A"):
    """Safely extracts nested values from a dictionary.

    Handles missing keys, explicit None values, and list indexing.
    """
    for key in keys:
        if isinstance(data, dict) and not isinstance(key, int):
            data = data.get(key)
        elif isinstance(data, list) and isinstance(key, int):
            try:
                data = data[key]
            except IndexError:
                return default
        else:
            return default
    return data if data is not None else default


def format_egypt_phone(phone):
    phone_str = str(phone).strip().replace(".0", "")

    if phone_str.startswith("+"):
        phone_str = phone_str[1:]
    elif phone_str.startswith("00"):
        phone_str = phone_str[2:]

    if phone_str.startswith("01") and len(phone_str) == 11:
        return f"+20{phone_str[1:]}"

    if phone_str.startswith("1") and len(phone_str) == 10:
        return f"+20{phone_str}"

    if phone_str.startswith("201") and len(phone_str) == 12:
        return f"+{phone_str}"

    return f"+{phone_str}"


data = []

pagenum = 1

while pagenum <= 500:
    try:
        params = {
            "page": f"{pagenum}",
            "categorySlug": "%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
            "propertyTypeSlug": "%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA",
            "saleType": "%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
            "pattern": "/categorySlug/propertyTypeSlug-saleType.html",
        }

        response = requests.get(
            "https://www.propertyfinder.eg/search/_next/data/n09y_LvMgXM9OJRHS7qKz/ar/%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%A8%D9%8A%D8%B9.html.json",
            params=params,
            cookies=cookies,
            headers=headers,
            impersonate="chrome",
        )
        print(f"Response: {response.status_code}. Currently on Page: {pagenum}")
        pagenum += 1
        for item in response.json()["pageProps"]["searchResult"]["listings"]:
            price = safe_get(item, ["property", "price", "value"], default=None)
            if price is None or price == "None":
                continue
            description = safe_get(item, ["property", "description"])
            bedrooms = safe_get(item, ["property", "bedrooms"])
            bathrooms = safe_get(item, ["property", "bathrooms"])
            sqm = safe_get(item, ["property", "size", "value"])
            url = safe_get(item, ["property", "share_url"], default=None)
            itemproperty = item.get("property")
            if itemproperty:
                downpayment = (
                    itemproperty.get("down_payment_price")
                    if itemproperty.get("down_payment_price")
                    else "Not Specified"
                )
            for location in item.get("property", {}).get("location_tree"):
                if location.get("type") == "CITY":
                    city = " ".join(location.get("slug_en", None).split("-")).title()
                elif location.get("type") == "TOWN":
                    town = " ".join(location.get("slug_en", None).split("-")).title()
            # location = " ".join(unquote(raw_location_slug).split("-")) if raw_location_slug else "None"

            agent_name = safe_get(item, ["property", "agent", "name"])
            agent_phone = safe_get(item, ["property", "contact_options", 1, "value"])

            broker_name = safe_get(item, ["property", "broker", "name"])
            broker_phone = safe_get(item, ["property", "broker", "phone"])

            broker_phone = format_egypt_phone(broker_phone)
            agent_phone = format_egypt_phone(agent_phone)

            furnished = safe_get(item, ["property", "furnished"])
            if not furnished or furnished == "None":
                furnished = None
            if bedrooms == unquote("\u0633\u062a\u0648\u062f\u064a\u0648"):
                bedrooms = 0
            data.append(
                {
                    "Property Description": f"{description[:200]}...",
                    "Price (EGP)": price,
                    "Downpayment Price (EGP)": downpayment,
                    "Price per SQM": price // sqm,
                    "City": city,
                    "Town": town,
                    "Bedrooms": bedrooms,
                    "Bathrooms": bathrooms,
                    "Property Size (SQM)": sqm,
                    "Furnishing Status": furnished,
                    "Agent Name": agent_name,
                    "Agent Phone": agent_phone,
                    "Broker Name": broker_name,
                    "Broker Phone": broker_phone,
                    "Listing URL": url,
                }
            )
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print("Error: " + e)
        df = pd.DataFrame(data)
        df.to_csv("propertyfinder.csv", index=False)


df = pd.DataFrame(data)
df.to_csv("propertyfinderextreme.csv", index=False)
