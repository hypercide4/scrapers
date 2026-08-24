## Web Scraping and Data Extraction Toolkit

A collection of Python-based web scrapers and API parsers scripts showing progressive data extraction techniques ranging from static HTML parsing to simple anti-bot evasion and backend API reverse-engineering.

## Libraries
* Data Handling: `pandas`
* Static Parsing: `BeautifulSoup`, `lxml`
* Dynamic Rendering: `Playwright`
* HTTP Requests & Anti-Bot Evasion: `requests`, `curl_cffi` (for Chrome TLS impersonation)

---

## Repository Structure

The scripts are categorized by the complexity of the scraping challenge:

### 1. Static Parsing & Pagination
* `books_to_scrape.py`: Scrapes basic book titles, prices, and star ratings across multiple catalog pages using `BeautifulSoup` and custom mapping dictionaries.
* `books_to_scrape_2.py`: An advanced version that goes into individual product pages to extract detailed descriptions, UPCs, tax amounts, and availability counts.
* `amazon.py`: Same as above (`books_to_scrape_2.py`) but on a real page example.

### 2. AJAX and API Endpoints
* `movies_scraper.py`: Fetches awards, nominations, and "Best Picture" data directly from JSON endpoints year by year.
* `cars_ajax_scraper.py`: Iterates through car brands, categories, and paginated AJAX responses to gather vehicle details.
* `dockland.py`: Directly targets Shopify product JSON endpoints to pull inventory variants, prices, colors, and sizes.

### 3. Dynamic Rendering 
* `quotes_to_scrape_dynamic.py`: Uses `playwright` to wait for elements to load in with JavaScript and scrapes the JavaScript-rendered quote pages.

### 4. More Advanced Reverse-Engineering
* `propertyfinder.py`: Uses `curl_cffi` for Chrome TLS impersonation, uses a safe navigation helper (`safe_get`), cleans regional phone numbers, and handles large-scale real estate listings.
* `trip_advisor_scrape.py`: Intercepts network post requests to target GraphQL query endpoints with payloads, offset management and rate-limit handling.

## Installation:

* Clone the Repository:
```bash
git clone https://github.com/hypercide4/web-scraping-portfolio.git
cd web-scraping-portfolio
```

* Install Dependencies:
```
pip install pandas requests beautifulsoup4 lxml curl_cffi playwright
playwright install

```

## Usage:

For the simpler scripts you can immediately run:
```bash
python dockland.py

```
### Advanced Setup: Extracting Cookies & Headers 

For advanced scripts that require specific authentication cookies and headers, follow these steps to capture the necessary network data:
1. Open Developer Tools 
* Press `F12` in your browser.
* Navigate to the Network tab.
2. Trigger the Network Request
* Refresh the page or scroll down to load new content.
* Look for incoming Fetch/XHR or JSON requests in the log.
* Click on the requests and check the Response tab to ensure it contains the data you need.
3. Copy the Request
* Right-click the correct network request.
* Select Copy > Copy as cURL (bash).
4. Convert the cURL Command
* Paste the copied cURL command into `curlconverter.com`.
* Select Python to generate the cookies and headers.
5. Update the Script
* Copy the generated `headers`, `cookies`, and `payload/query` data.
* Paste them into your local script configuration.
* Run the script as usual

## Disclaimer:

This repository was created strictly for educational purposes and technical demonstration. Please adhere to website Terms of Service and robots.txt guidelines when you are web-scraping.
