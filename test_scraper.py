
import csv
import json
import os


def test_project():

    print("PROJECT TESTING")
    print("================")

    csv_path = "output/products.csv"
    json_path = "output/products.json"

    # Check CSV
    if os.path.exists(csv_path):

        with open(
            csv_path,
            "r",
            encoding="utf-8-sig"
        ) as file:

            csv_data = list(csv.DictReader(file))

        print("CSV file: PASS")
        print("CSV records:", len(csv_data))

        if len(csv_data) >= 100:
            print("Minimum 100 records: PASS")
        else:
            print("Minimum 100 records: FAIL")

        titles = [
            book["title"] for book in csv_data
        ]

        if len(titles) == len(set(titles)):
            print("Duplicate check: PASS")
        else:
            print("Duplicate check: FAIL")

    else:
        print("CSV file: FAIL")

    # Check JSON
    if os.path.exists(json_path):

        try:
            with open(
                json_path,
                "r",
                encoding="utf-8"
            ) as file:

                json_data = json.load(file)

            print("JSON file: PASS")
            print("JSON records:", len(json_data))

        except json.JSONDecodeError:
            print("JSON validation: FAIL")

    else:
        print("JSON file: FAIL")

    print("================")
    print("TESTING COMPLETED")


if __name__ == "__main__":
    test_project()
