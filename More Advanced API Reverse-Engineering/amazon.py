import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests

cookies = {} # replace with curl cookies
headers = {} # replace with curl headers

data = []
pagenum = 1
while pagenum <= 2:
    url = f"https://www.amazon.com/s?k=earbuds&page={pagenum}&xpid=Y04stg21Zfalz&crid=M38IUB6BBTV1&qid=1787516428&refresh=2&sprefix=earbu%2Caps%2C316&ref=sr_pg_{pagenum - 1 if pagenum > 1 else 1}"

    req = requests.get(url, impersonate="chrome", headers=headers, cookies=cookies)
    print(f"RESPONSE CODE: {req.status_code} CURRENTLY ON PAGE: {pagenum}")
    html = BeautifulSoup(req.text, "lxml")

    products = html.find_all(
        "div",
        class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small gsx-ies-anchor sg-col-12-of-16",
        attrs=({"role": "listitem"}),
    )
    # try:
    for product in products:
        name = product.select_one("div[data-cy='title-recipe'] a h2 span").text.strip()
        price = product.find("span", class_="a-offscreen")
        if price:
            price = float(price.text.replace("$", ""))
        else:
            continue
        rating = product.find("span", class_="a-size-small a-color-base")
        if rating:
            rating = rating.text
        else:
            rating = 0
        reviewcount = (
            product.find(
                "span",
                class_=["a-size-mini", "puis-normal-weight-text", "s-underline-text"],
            )
            .text.replace("(", "")
            .replace(")", "")
            .replace("K", "")
        )
        if "." in reviewcount and reviewcount != "":
            reviewcount.replace(".", "")
            reviewcount = float(reviewcount)
            reviewcount *= 1000
        else:
            if reviewcount != "":
                reviewcount = float(reviewcount)
            elif reviewcount == "":
                reviewcount = 0.0
        url_path = product.find(
            "span", attrs=({"data-component-type": "s-product-image"})
        ).a["href"]
        product_url = f"www.amazon.com/{url_path}"
        asin = product_url.split("/")[4]
        data.append(
            {
                "Name": name,
                "Price": price,
                "Rating": rating,
                "Review Count": reviewcount,
                "URL": product_url,
                "ASIN": asin,
            }
        )
    pagenum += 1
# except:
df = pd.DataFrame(data)
df_cleaned = df.drop_duplicates(subset=["ASIN"])
df.to_csv("amazon products.csv", index=True)

# df = pd.DataFrame(data)
# df.to_csv("amazon products.csv", index=False)
