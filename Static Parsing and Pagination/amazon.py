import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests

cookies = {
    "session-id": "141-3520421-0045012",
    "session-id-time": "2082787201l",
    "lc-main": "en_US",
    "ubid-main": "133-0311379-7201356",
    "sst-main": "Sst1|PQJnKx3Vgwh-PJiRvmY4jh6NB9GMoou8ay4cU7rN8FbUejf-4GENYWP3ZTXeEJb-VyWfOemgOa3K3oimY-iOqoJnFKRjuR74W6Nh5RjdEPReU8-SOQe-OUOjC7xN7HzzPsz4lDIMz0zrezk9Biv3Hdk2lGus28NYod6YgCzALv1L_XZjKJ1gAV1-XvYIscoBUgw67tuEgMr5Mr3ZnRObFB8qbFiO_Uqs-JRoUa8kv3o6qT8OTWDAthL0dwP2q4PGEE0p",
    "skin": "noskin",
    "Lda_aKUr6BGRn": "duertry.com/r/v2?",
    "Lda_aKUr6BGRr": "1",
    "i18n-prefs": "USD",
    "session-token": "AEBpp9QpVYtAPS/ClyUfrXSmNdUaFgiL27wo/jZXizxeQ/ewlkOo9SjCeMfGB67gU56LWgXagEUCuSa/EIqwaxG9tRjfE2Y/GEVkYeo48065MSJ6PBGpfBiPapO5XSUCrrcXmvaaPYmiu5IeK6VUQO6kiSdZAQCggAzLr1MJmU8LzPvuHIIoiUVjpg0bpQdU5oshhE/e/Zd8gX9OjaaKBz0n1Frqchc2",
    "csm-hit": "adb:adblk_yes&t:1787520026559&tb:BGW5QMNQ5XF80KQY1Q59+s-WWFXK8GENNZRFXEVFHJV|1787520026559",
    "cmc": "xs0wpvkuchog7IKc1tyXsLrkdfNiQHELjyFmV1DAvlBwnP8b5wVTRA0Wm3LGGon1ZxXh3/NQNDwR7V2Z2DUtAdsqVt4mMNWz6IB4o/AUM1x4i9EYmOOT3Qc1so1a5BrPXIdiy+EBaT6JVDOCMMqcrQXhTOyPLxLXnFRugjxwvT82uLPTKxXBsOr1jf4azybPgQGa9VDFw9t0OGzBq4rACi4fezlytIHCrL3rGi4TaX8tmIR0BckF8b62jhL3Rg3CNkNK2Y7PHcfrULNs7rLDixIwgjU=",
    "rxc": "AEZAHMHmfgv/RinYqyQ",
}

headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Origin": "https://www.amazon.com",
    "Pragma": "no-cache",
    "Referer": "https://www.amazon.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

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
