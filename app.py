import os
from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

HOST = "0.0.0.0"

PORT = 5000

# Define the path to the database
DATABASE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 
    'database', 
    'database.db')

# Ensure the 'database' folder exists
if not os.path.exists(os.path.dirname(DATABASE)):
    os.makedirs(os.path.dirname(DATABASE))

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        g._database = db
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for users page
@app.route('/users')
def users():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    return render_template('users.html', users=users)

# Route to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        db = get_db()
        db.execute("INSERT INTO user (name) VALUES (?)", (name,))
        db.commit()
        return redirect(url_for('users'))
    return render_template('add_user.html')

# Route to initialize the database
@app.route('/initdb')
def initdb():
    with app.app_context():
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT)')
        db.commit()
    return 'Database initialized!'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
