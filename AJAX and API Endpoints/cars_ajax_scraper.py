import pandas as pd
import requests
from bs4 import BeautifulSoup

data = []

cookies = {}  # replace with curl cookies

headers = {}  # replace with curl headers

for car in [
    "BMW",
    "Ferrari",
    "Ford",
    "Jaguar",
    "Mercedez-Benz",
    "Nissan",
    "Porsche",
    "Toyota",
]:
    for category in ["Convertible", "Hatchback", "Coupe", "Sedan"]:
        page_num = 1
        while True:
            params = {
                "page": page_num,
            }
            response = requests.get(
                f"https://webscraper.io/test-sites-ajax/{car}/{category}",
                params=params,
                headers=headers,
                cookies=cookies,
            )
            print(
                f"on the page: https://webscraper.io/test-sites-ajax/{car}/{category}"
            )
            page_num += 1
            soup = BeautifulSoup(response.text, "lxml")
            cards = soup.find_all("div", class_="col-md-4 col-xl-4 col-lg-4")
            if not cards:
                break
            for card in cards:
                availability = card.find("div", class_="badge").text.strip()
                price = card.find(
                    "p", class_="price col-6 mb-0 text-end p-0"
                ).span.text.replace("USD ", "$")
                description = card.find(
                    "p", class_="description text-muted"
                ).text.strip()
                rating = card.find(
                    "div",
                    class_="col-6 rarity-rating d-flex flex-row justify-content-start p-0",
                )["data-rating"]
                name = card.h3.a.text.strip()

                data.append(
                    {
                        "Name": name,
                        "Price": price,
                        "Rating": rating,
                        "Availability": availability,
                        "Description": description,
                    }
                )

df = pd.DataFrame(data)
df.to_csv("cars.csv", index=False)
