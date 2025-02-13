from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from database import create_user, check_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if create_user(email, hashed_pw):
            return redirect(url_for('login'))
        else:
            return "User already exists!"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email)

        if user and bcrypt.check_password_hash(user[1], password):
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome, {session['user']}! <br><a href='/logout'>Logout</a>"
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
