import re

import pandas as pd
from curl_cffi import requests

data = []
with requests.Session() as session:
    response = session.get(
        "https://www.dockland.com.eg/products.json?page=1&limit=250",
        impersonate="chrome",
    )

    for product in response.json()["products"]:
        sizes = set()
        image_link = []
        colors = set()
        link = f"https://www.dockland.com.eg/products/{product['handle']}"
        name = product["title"].strip().title().replace("  ", " ")
        price = product["variants"][0]["price"]
        old_price = (
            product["variants"][0]["compare_at_price"]
            if product["variants"][0]["compare_at_price"]
            else price
        )
        on_sale = "YES" if old_price > price else "NO"
        category = product["product_type"].title()
        image_link = product["images"][0]["src"]
        for variant in product["variants"]:
            if variant["available"]:
                colors.add(variant["option1"].title())
                sizes.add(variant["option2"].upper())
        in_stock = "NO" if not colors and not sizes else "YES"
        sizes = sorted(sizes)
        colors = sorted(colors)
        sizes = ", ".join(sizes)
        colors = ", ".join(colors)
        if in_stock == "NO":
            colors = "Out of Stock"
            sizes = "Out  of Stock"
        if not category:
            category = "Polo"
        if re.search("Jeans", name):
            category = "Jeans"
        elif re.search("Short-Sleeve", name):
            category = "T-Shirt"
        elif re.search("Sweatpants", name):
            category = "Sweatpants"
        elif re.search("Chino", name):
            category = "Chino"
        elif re.search("Long Sleeve", name):
            category = "Long Sleeve T-Shirt"

        data.append(
            {
                "Item Name": name,
                "Category / Type": category,
                "Price (EGP)": price,
                "Original Price (EGP)": old_price,
                "On Sale": on_sale,
                "Available Colors": colors.replace("  ", " "),
                "Available Sizes": sizes,
                "In Stock": in_stock,
                "Web Link": link,
                "Picture Link": image_link,
            }
        )

df = pd.DataFrame(data)
df.to_excel("dockland_data.xlsx", index=False)
