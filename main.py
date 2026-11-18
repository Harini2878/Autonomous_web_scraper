
import csv
import json
import os

from scraper import scrape_books


def save_data(books):

    os.makedirs("output", exist_ok=True)

    if not books:
        print("No data available to save!")
        return

    # Save CSV
    csv_file = "output/products.csv"

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=books[0].keys()
        )

        writer.writeheader()
        writer.writerows(books)

    print("CSV file saved successfully!")

    # Save JSON
    json_file = "output/products.json"

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            books,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("JSON file saved successfully!")


def main():

    print("AUTONOMOUS WEB SCRAPER")
    print("======================")

    books = scrape_books()

    print("\nTotal records:", len(books))

    save_data(books)

    print("\nProject execution completed!")


if __name__ == "__main__":
    main()
