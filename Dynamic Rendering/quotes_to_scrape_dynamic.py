import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

data = []
counter = 1
while counter <= 10:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://quotes.toscrape.com/js/page/{counter}")
        page.wait_for_selector(".quote")
        html = page.inner_html(".container")
        soup = BeautifulSoup(html, "lxml")

    quotes = soup.find_all("div", class_="quote")
    for quote in quotes:
        quote_info = quote.find("span", class_="text")
        author_name = quote_info.find_next_sibling("span").small.text
        quote_text = quote_info.get_text()
        tags = quote.find_all("a", class_="tag")
        cleaned_tags = []
        for tag in tags:
            tag_text = tag.text
            cleaned_tags.append(tag_text)
        finished_tags = ", ".join(cleaned_tags)
        data.append(
            {
                "Quote": quote_text.strip(),
                "Author": author_name.strip(),
                "Tags": finished_tags.strip(),
            }
        )

    counter += 1

df = pd.DataFrame(data)
df.to_csv("quotes.csv", index=False)
