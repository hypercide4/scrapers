import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests

cookies = {}  # replace with curl cookies
headers = {}  # replace with curl headers

data = []
pagenum = 1


def parse_review_count(val):
    if pd.isna(val):
        return 0

    val = str(val).strip().lower().replace(",", "").replace("(", "").replace(")", "")
    multiplier = 1

    if "k" in val:
        multiplier = 1000
        val = val.replace("k", "")
    elif "m" in val:
        multiplier = 1000000
        val = val.replace("m", "")

    try:
        return int(float(val) * multiplier)
    except ValueError:
        return 0


try:
    while pagenum <= 1:
        url = f"https://www.amazon.com/s?k=iphone&page={pagenum}&xpid=kwBxfNk-AIxs0&crid=3F2HPTXP1VABZ&qid=1787557765&sprefix=iphone%2Caps%2C270&ref=sr_pg_{pagenum - 1 if pagenum > 1 else 1}"

        req = requests.get(url, impersonate="chrome", headers=headers, cookies=cookies)
        print(f"RESPONSE CODE: {req.status_code} CURRENTLY ON PAGE: {pagenum}")

        html = BeautifulSoup(req.text, "lxml")
        products = html.find_all(
            "div",
            class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small gsx-ies-anchor sg-col-12-of-16",
            attrs={"role": "listitem"},
        )
        has_item = []

        for product in products:
            name_el = product.select_one("div[data-cy='title-recipe'] a h2 span")
            if not name_el:
                continue
            name = name_el.text.strip()

            price_el = product.find("span", class_="a-offscreen")
            if not price_el:
                continue
            price = float(price_el.text.replace("$", "").replace(",", ""))

            prime_el = product.find(
                "a",
                class_="prime-signup-ingress",
                attrs={"data-client-id": "UdmDeliveryBlockMedium"},
            )
            is_prime = bool(prime_el)

            rating_el = product.find("span", class_="a-size-small a-color-base")
            rating = rating_el.text if rating_el else 0

            review_el = product.find(
                "span",
                class_=["a-size-mini", "puis-normal-weight-text", "s-underline-text"],
            )
            review_count = (
                review_el.text.replace("(", "").replace(")", "") if review_el else 0
            )
            review_count = parse_review_count(review_count)

            img_el = product.find(
                "div", class_="a-section aok-relative s-image-fixed-height"
            )
            img_url = img_el.img["src"] if img_el and img_el.img else ""

            path_el = product.find(
                "span", attrs={"data-component-type": "s-product-image"}
            )
            if not path_el or not path_el.find("a"):
                continue

            product_url = f"https://www.amazon.com{path_el.a['href']}".split("/ref")[0]
            asin = product_url.split("/")[5]

            detail_req = requests.get(
                product_url, impersonate="chrome", headers=headers, cookies=cookies
            )
            detail_html = BeautifulSoup(detail_req.text, "lxml")

            list_price_el = detail_html.find(
                "span", class_="a-price a-text-price apex-basisprice-value"
            )
            list_price = (
                float(list_price_el.span.text.replace("$", ""))
                if list_price_el and list_price_el.span
                else price
            )

            brand_name = name.split(" ")[0]
            color = "Unspecified"
            bsr = "Unspecified"

            for row in detail_html.find_all("tr"):
                if row.td and row.th:
                    th_text = row.th.text.strip()
                    td_text = row.td.text.strip()
                    if th_text == "Best Sellers Rank":
                        bsr = td_text
                    elif th_text == "Brand Name":
                        brand_name = td_text
                    elif th_text == "Color":
                        color = td_text

            ranks = [int(num.replace(",", "")) for num in re.findall(r"#([\d,]+)", bsr)]
            main_rank = ranks[0] if len(ranks) > 0 else None
            sub_rank = ranks[1] if len(ranks) > 1 else None

            name = name.split("|")[0].split(",")[0].split(" - ")[0]
            if name == "Wireless Earbuds":
                name = f"{brand_name} Generic Wireless Earbuds"

            if (
                main_rank is None
                or sub_rank is None
                or main_rank > 10000
                or sub_rank > 10000
            ):
                continue

            sale_pct = round((1 - (price / list_price)) * 100, 2)

            product_data = {
                "Name": name,
                "Price/Currency": "USD",
                "Price/Value": price,
                "ListPrice/Value": list_price,
                "Sale (%)": sale_pct,
                "Brand": brand_name,
                "Rating": rating,
                "Review Count": int(review_count),
                "ASIN": asin,
                "Main Rank": main_rank,
                "Sub Rank": sub_rank,
                "Color": color,
                "isPrime": is_prime,
                "URL": product_url,
                "Image URL": img_url,
                "Date Scraped": "2026-08-24",
            }

            data.append(product_data)
            has_item.append(product_data)

            print(f"Appended: {name} | Price: {price} | Rank: {main_rank}/{sub_rank}")

        if not has_item:
            print("Waiting A/B testing....")
            time.sleep(30)
            continue

        pagenum += 1

finally:
    if data:
        df = pd.DataFrame(data).drop_duplicates(subset=["ASIN"])
        df_sorted = df.sort_values(by=["Main Rank", "Sub Rank"], ascending=True)

        file_name = "phone.xlsx"
        with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
            df_sorted.to_excel(writer, sheet_name="Products", index=False)
            worksheet = writer.sheets["Products"]

            for col in worksheet.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)
