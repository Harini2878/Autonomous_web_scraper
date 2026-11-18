
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_page(url, retries=3):

    for attempt in range(retries):

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            response.raise_for_status()
            return response

        except requests.RequestException as error:

            print(f"Attempt {attempt + 1} failed: {error}")

            if attempt < retries - 1:
                time.sleep(2)

    print("Maximum retries reached!")
    return None


def scrape_books():

    all_books = []
    url = BASE_URL
    page_number = 1

    while url:

        print(f"\nScraping page {page_number}...")

        response = get_page(url)

        if response is None:
            print("Scraping stopped due to connection error.")
            break

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        books = soup.find_all(
            "article",
            class_="product_pod"
        )

        for book in books:

            try:
                title = book.h3.a["title"]

                price = book.find(
                    "p",
                    class_="price_color"
                ).get_text(strip=True)

                availability = book.find(
                    "p",
                    class_="instock availability"
                ).get_text(strip=True)

                rating_tag = book.find(
                    "p",
                    class_="star-rating"
                )

                rating = (
                    rating_tag.get("class", ["Unknown"])[1]
                    if rating_tag and len(rating_tag.get("class", [])) > 1
                    else "Unknown"
                )

                all_books.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "availability": availability
                })

            except (AttributeError, KeyError, TypeError) as error:

                print("Invalid book skipped:", error)
                continue

        print("Total books collected:", len(all_books))

        next_button = soup.find(
            "li",
            class_="next"
        )

        if next_button:

            next_link = next_button.a["href"]
            url = urljoin(url, next_link)
            page_number += 1

        else:
            url = None

        time.sleep(1)

    print("\nScraping completed!")
    return all_books
