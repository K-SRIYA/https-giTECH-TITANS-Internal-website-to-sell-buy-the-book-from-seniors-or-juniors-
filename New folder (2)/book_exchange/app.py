from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, price REAL, seller TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS cart
                 (id INTEGER PRIMARY KEY, book_id INTEGER, user_id INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add authentication logic here
        return redirect(url_for('catalog'))
    return render_template('login.html')

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = float(request.form['price'])
        seller = 'default_seller'  # Replace with actual seller logic
        c.execute('INSERT INTO books (title, author, price, seller) VALUES (?, ?, ?, ?)',
                  (title, author, price, seller))
        conn.commit()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    return render_template('catalog.html', books=books)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        user_id = 1  # Replace with actual user ID logic
        conn = sqlite3.connect('books.db')
        c = conn.cursor()
        c.execute('INSERT INTO cart (book_id, user_id) VALUES (?, ?)', (book_id, user_id))
        conn.commit()
        conn.close()
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''SELECT books.id, books.title, books.author, books.price 
                 FROM books INNER JOIN cart ON books.id = cart.book_id WHERE cart.user_id = ?''', (1,))
    cart_items = c.fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Process payment logic here
        return redirect(url_for('home'))
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
