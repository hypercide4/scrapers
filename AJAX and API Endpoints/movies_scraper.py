import pandas as pd #noqa
import requests
import json

data = []
headers={
    "Sec-Ch-Ua": 'Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
}
years = 2010
while years<=2015:
    url = f'https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={years}'

    resp = requests.get(url, headers=headers)
    item_list = json.loads(resp.text)
    for index, item in enumerate(item_list):
        title = item["title"]
        year = item["year"]
        awards = item["awards"]
        nominations = item["nominations"]
        try:
            best_picture = item["best_picture"]
        except KeyError:
            ''
        data.append({
            "Title": title,
            "Year": year,
            "Awards": awards,
            "Nominations": nominations,
            "Best Picture": "Yes" if best_picture else "No"
        })
        best_picture = ""
    years+=1
df = pd.DataFrame(data)
df.to_csv("movies.csv", index=False)

