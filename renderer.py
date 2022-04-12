from flask import Flask
from flask import render_template
from flask import send_from_directory
import psycopg2

app = Flask(__name__)

@app.route("/style.css")
def css():
    return send_from_directory('reports', 'style.css')

@app.route("/showcase.png")
def png():
    return send_from_directory('reports', 'showcase.png')

@app.route("/index")
def display_index():
    connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books;')
    books = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("index.html")

@app.route("/submitForm")
def display_submit():
    return render_template("submitForm.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
