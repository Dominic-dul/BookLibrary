from multiprocessing import connection
import uuid
from flask import Flask, redirect, request, send_from_directory
from flask import render_template
import psycopg2

app = Flask(__name__)

@app.route("/style.css")
def css():
    return send_from_directory('reports', 'style.css')

@app.route("/showcase.png")
def png():
    return send_from_directory('reports', 'showcase.png')


# @app.route("/index")
# def display_index():
#     connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")

#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM books;')
#     books = cursor.fetchall()
#     cursor.close()
#     connection.close()

#     return render_template("index.html")

@app.route("/books")
def show_books():
    connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books;')
    books_from_db = cursor.fetchall()
    cursor.close()
    connection.close()

    nob = len(books_from_db)
    return render_template("books.html", books = books_from_db, numberOfBooks = nob)

@app.route("/book/delete/<book_id>")
def delete_book(book_id):
    connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM books WHERE book_id = '{book_id}'")
    cursor.close()
    connection.close()
 
    return redirect("/books")

@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template("newBook.html")
    if request.method == "POST":
        id = str(uuid.uuid4())
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")

    connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (book_id, book_name, book_author, book_release) VALUES (%s, %s, %s, %s)", (id, title, author, year))
    cursor.close()
    connection.close()

    return redirect("/books")

@app.route("/book/modify/<book_id>", methods=["GET", "POST"])
def modify_book(book_id):
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        single_book = cursor.fetchone()
        print(single_book)
        cursor.close()
        connection.close()

        return render_template("modifyBook.html", book = single_book)

    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        connection = psycopg2.connect(host="localhost", database="BooksDatabase", user="postgres", password="12344")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET book_name = %s, book_author = %s, book_release = %s WHERE book_id = %s", (title, author, year, book_id))
        cursor.close()
        connection.close()

    return redirect("/books")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
