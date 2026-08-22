import random
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    "Sec-Ch-Ua": 'Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
}

STAR_RATING_MAP = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5"}

data = []

catalogue_url = "http://books.toscrape.com/catalogue/"

counter = 1
while counter <= 50:
    url = f"http://books.toscrape.com/catalogue/page-{counter}.html"
    print(f"on page {counter}")
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book in books:
        if book.find("article"):
            book_title = book.article.h3.a["title"].strip()
            book_url = f"{catalogue_url}{book.article.h3.a['href'].strip()}"
            book_price = (
                book.article.find("div", class_="product_price")
                .p.text.replace("Â", "")
                .strip()
            )
            book_availability = book.article.find(
                "p", class_="instock availability"
            ).text.strip()
            book_rating = book.article.p["class"][1].replace("star-rating", "").strip()
            for word, digit in STAR_RATING_MAP.items():
                book_rating = book_rating.replace(word, digit)
            data.append(
                {
                    "Title": book_title,
                    "Price (excl. tax)": book_price,
                    "Price(incl. tax)": "",
                    "Tax Amount": "",
                    "Availability Count": "",
                    "Number of Reviews": "",
                    "Full Description": "",
                }
            )
    counter += 1
    time.sleep(random.uniform(1,2))

df = pd.DataFrame(data)

df.to_csv("books.csv", index=False)
