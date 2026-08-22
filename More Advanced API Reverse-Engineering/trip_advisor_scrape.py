import random
import time

import pandas as pd
from curl_cffi import requests

cookies = {}  # replace with curl cookies
headers = {}  # replace with curl headers

try:
    data = []
    offset = 30
    while offset <= 2691:
        GraphQL_Query = [
            {
                "variables": {
                    "page": "Restaurants",
                    "pos": "en-US",
                    "parameters": [
                        {
                            "key": "geoId",
                            "value": "294201",
                        },
                        {
                            "key": "offset",
                            "value": f"{offset}",
                        },
                    ],
                    "factors": [
                        "TITLE",
                        "META_DESCRIPTION",
                        "MASTHEAD_H1",
                        "MAIN_H1",
                        "IS_INDEXABLE",
                        "RELCANONICAL",
                    ],
                    "route": {
                        "page": "Restaurants",
                        "params": {
                            "geoId": 294201,
                            "offset": f"{offset}",
                        },
                    },
                    "currencyCode": "USD",
                },
                "extensions": {
                    "preRegisteredQueryId": "18d4572907af4ea5",
                },
            },
            {
                "variables": {
                    "limit": 30,
                    "racRequest": None,
                    "route": {
                        "page": "Restaurants",
                        "params": {
                            "geoId": 294201,
                            "offset": f"{offset}",
                        },
                    },
                    "additionalSelections": [
                        {
                            "facet": "ESTABLISHMENT_TYPES",
                            "selections": [
                                "10591",
                            ],
                        },
                    ],
                    "insertSponsoredListings": True,
                    "avoidLSS": False,
                    "locale": "en-US",
                },
                "extensions": {
                    "preRegisteredQueryId": "7c7457de6bd4ad87",
                },
            },
            {
                "variables": {
                    "pageName": "Restaurants",
                    "relativeUrl": "/Restaurants-g294201-oa30-Cairo_Cairo_Governorate.html",
                    "parameters": [
                        {
                            "key": "geoId",
                            "value": "294201",
                        },
                        {
                            "key": "offset",
                            "value": f"{offset}",
                        },
                    ],
                    "route": {
                        "page": "Restaurants",
                        "params": {
                            "geoId": 294201,
                            "offset": f"{offset}",
                        },
                    },
                    "routingLinkBuilding": True,
                },
                "extensions": {
                    "preRegisteredQueryId": "211573a2b002568c",
                },
            },
            {
                "variables": {
                    "geoId": 294201,
                },
                "extensions": {
                    "preRegisteredQueryId": "cdffe732d76767aa",
                },
            },
            {
                "variables": {
                    "page": "Restaurants",
                    "params": [
                        {
                            "key": "geoId",
                            "value": "294201",
                        },
                        {
                            "key": "offset",
                            "value": f"{offset}",
                        },
                    ],
                    "route": {
                        "page": "Restaurants",
                        "params": {
                            "geoId": 294201,
                            "offset": f"{offset}",
                        },
                    },
                },
                "extensions": {
                    "preRegisteredQueryId": "f742095592a84542",
                },
            },
            {
                "variables": {
                    "events": [
                        {
                            "schemaName": "user_impression",
                            "eventJson": '{"producer_ref":"web-platform-domain","impression_id":"ee374d0c-f902-4dd5-ba91-e51b23bfd3bd","client_timestamp_ms":1787350422100,"page_view_id":"DEPRECATED","team":"Other","ta_unique_id":"DEPRECATED","member_id":"DEPRECATED","session_id":"18DB6F63507B02532EC189A19BEF224B","locale":"en-US","user_agent":"DESKTOP","page":"Restaurants","item_name":"Rewards","item_type":"Rewards","custom_data":"{\\"isGeoScoped\\":true,\\"isStickied\\":false,\\"isSignedIn\\":false,\\"parentItemType\\":\\"Header\\"}","page_uid":"05c100be-b4c9-4743-a187-0b152d806af8","client_timestamp":"2026-08-22 01:13:42.100"}',
                        },
                    ],
                },
                "extensions": {
                    "preRegisteredQueryId": "71a4406fb83d70a3",
                },
            },
            {
                "variables": {
                    "events": [
                        {
                            "schemaName": "user_impression",
                            "eventJson": '{"producer_ref":"web-platform-domain","impression_id":"3ab7e662-754f-4dfb-b3a3-e9f1374a7bdf","client_timestamp_ms":1787350422100,"page_view_id":"DEPRECATED","team":"Other","ta_unique_id":"DEPRECATED","member_id":"DEPRECATED","session_id":"18DB6F63507B02532EC189A19BEF224B","locale":"en-US","user_agent":"DESKTOP","page":"Restaurants","item_name":"NoLoginSaves","item_type":"NoLoginSaves","custom_data":"{\\"isGeoScoped\\":true,\\"isStickied\\":false,\\"isSignedIn\\":false,\\"parentItemType\\":\\"Header\\"}","page_uid":"05c100be-b4c9-4743-a187-0b152d806af8","client_timestamp":"2026-08-22 01:13:42.100"}',
                        },
                    ],
                },
                "extensions": {
                    "preRegisteredQueryId": "71a4406fb83d70a3",
                },
            },
        ]
        try:
            response = requests.post(
                "https://www.tripadvisor.com/data/graphql/ids",
                cookies=cookies,
                headers=headers,
                json=GraphQL_Query,
                impersonate="chrome",
            )
            if response.status_code == 429:
                print("too many requests")
                break
        except requests.errors.RequestsError as e:
            if 429 in str(e):
                print("EXCEPT ERROR")
                break
        print(f"on page: {offset // 30}")
        restaurants = (
            response.json()[1]["data"]["response"]["restaurants"]
            if len(response.json()) > 1
            else print("not enough data")
        )
        time.sleep(random.uniform(0.48, 0.93))
        for restaurant in restaurants:
            cuisines = []
            name = restaurant["name"]
            web_url = (
                f"https://www.tripadvisor.com/{restaurant['detailPageRoute']['url']}"
            )
            avg_rating = restaurant["reviewSummary"]["rating"]
            reviews = restaurant["reviewSummary"]["count"]
            location = restaurant["taLocation"]["contact"]["streetAddress"][
                "fullAddress"
            ]
            items = restaurant.get("priceTypes", {}).get("items", [])
            price_range = items[0]["secondaryName"] if items else "Not Listed"
            menu = restaurant["menu"]["menuUrl"]
            phone = restaurant["taLocation"]["contact"]["telephone"]
            for item in restaurant["cuisines"]["items"]:
                cuisines.append(item["tag"]["localizedName"])

            data.append(
                {
                    "Restaurant Name": name,
                    "Rating": avg_rating if avg_rating != -1 else "Not Rated",
                    "Review Count": reviews,
                    "Address": location,
                    "Cuisine Types": ", ".join(cuisines) if cuisines else "Not Listed",
                    "Price Range": price_range,
                    "Phone Number": phone if phone else "Not listed",
                    "Menu": menu if menu else "Not Listed",
                }
            )
        offset += 30
        time.sleep(random.uniform(1.5, 3))

except Exception:
    df = pd.DataFrame(data)
    df.to_excel("RestaurantData.xlsx", index=False)

df = pd.DataFrame(data)
df.to_excel("RestaurantData.xlsx", index=False)
