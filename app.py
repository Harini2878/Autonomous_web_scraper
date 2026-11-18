
from flask import Flask, render_template_string, send_from_directory
from scraper import scrape_books
from main import save_data
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Scraper Dashboard</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f6f9;
            padding: 30px;
        }

        .container {
            max-width: 1100px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
        }

        h1 { color: #243b55; }

        button {
            background: #2563eb;
            color: white;
            padding: 12px 22px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        a { margin-right: 15px; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 25px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }

        th { background: #243b55; color: white; }

        tr:nth-child(even) { background: #f2f2f2; }

        .count {
            font-size: 22px;
            margin: 20px 0;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Autonomous Web Scraper</h1>
    <p>Book Data Extraction Dashboard</p>

    <form action="/scrape" method="post">
        <button type="submit">Start Scraping</button>
    </form>

    <div class="count">
        Total Records: {{ count }}
    </div>

    {% if message %}
        <p>{{ message }}</p>
    {% endif %}

    {% if books %}
        <h2>Extracted Book Details</h2>

        <p>
            <a href="/download/products.csv">Download CSV</a>
            <a href="/download/products.json">Download JSON</a>
        </p>

        <table>
            <tr>
                <th>Book Title</th>
                <th>Price</th>
                <th>Rating</th>
                <th>Availability</th>
            </tr>

            {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.price }}</td>
                <td>{{ book.rating }}</td>
                <td>{{ book.availability }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}

</div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        books=[],
        count=0,
        message="Click Start Scraping to collect data."
    )


@app.route("/scrape", methods=["POST"])
def scrape():

    books = scrape_books()

    if books:
        save_data(books)

    message = "Scraping completed!" if books else "No records collected."

    return render_template_string(
        HTML,
        books=books,
        count=len(books),
        message=message
    )


@app.route("/download/<filename>")
def download(filename):

    if filename not in ["products.csv", "products.json"]:
        return "File not found", 404

    return send_from_directory(
        os.path.abspath("output"),
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
