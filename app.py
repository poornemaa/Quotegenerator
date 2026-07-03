from flask import Flask, render_template, redirect
import sqlite3
import requests

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS quotes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT,
            author TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():

    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()

    c.execute("SELECT * FROM quotes ORDER BY id DESC")

    history = c.fetchall()

    conn.close()

    return render_template("index.html", history=history)


@app.route('/generate')
def generate():

    response = requests.get("https://dummyjson.com/quotes/random")
    data = response.json()

    quote = data["quote"]
    author = data["author"]

    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO quotes(quote, author) VALUES(?, ?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return redirect('/')

    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO quotes(quote,author) VALUES(?,?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()

    c.execute("DELETE FROM quotes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/clear')
def clear():

    conn = sqlite3.connect("quotes.db")
    c = conn.cursor()

    c.execute("DELETE FROM quotes")

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)