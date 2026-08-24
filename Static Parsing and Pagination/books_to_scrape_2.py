import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

session = requests.Session()


session.headers.update(
    {
        "Sec-Ch-Ua": 'Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    }
)

counter = 1
url = f"http://books.toscrape.com/catalogue/page-{counter}.html"
data = []

while counter <= 3:
    response = session.get(url, timeout=(3, 10))
    soup = BeautifulSoup(response.text, "lxml")
    books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    for book in books:
        if book.find("article"):
            book_url = (
                f"http://books.toscrape.com/catalogue/{book.article.h3.a['href']}"
            )
            detail_response = session.get(book_url, timeout=(3, 10))
            detail_soup = BeautifulSoup(detail_response.text, "lxml")

            description_heading = detail_soup.find("div", id="product_description")
            full_description = description_heading.find_next_sibling("p").text

            title = detail_soup.find(
                "div", class_="col-sm-6 product_main"
            ).h1.text.strip()

            table = detail_soup.find("table", class_="table table-striped")
            rows = table.find_all("tr")

            upc = ""
            price_tax = ""
            price_no_tax = ""
            tax_amount = ""
            availability_count = ""
            number_of_reviews = ""

            for row in rows:
                if row.th.text == "UPC":
                    upc = row.td.text.strip()
                if row.th.text == "Price (excl. tax)":
                    price_no_tax = row.td.text.strip().replace("Â£", "")
                if row.th.text == "Price (incl. tax)":
                    price_tax = row.td.text.strip().replace("Â£", "")
                if row.th.text == "Availability":
                    availability_count = re.findall(r"\d+", row.td.text)[0]
                if row.th.text == "Number of reviews":
                    number_of_reviews = row.td.text.strip()
            tax_amount = str(float(price_tax) - float(price_no_tax)).strip()

            data.append(
                {
                    "URL": book_url,
                    "Title": title,
                    "UPC": upc,
                    "Price (excl. tax)": "£" + price_no_tax,
                    "Price (incl. tax)": "£" + price_tax,
                    "Tax Amount": "£" + tax_amount,
                    "Availability Count": availability_count,
                    "Number of Reviews": number_of_reviews,
                    "Full Description": full_description,
                }
            )
    counter += 1
    time.sleep(2)

df = pd.DataFrame(data)
df.to_csv("detailedbooks.csv", index=False)
