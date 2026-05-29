# frontend-service/app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = "shopcart-super-secret-key"

USER_SERVICE_URL    = os.getenv("USER_SERVICE_URL",    "http://localhost:5001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:5002")

@app.route('/')
def index():
    return render_template('index.html', user=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        payload = {
            "username": request.form['username'],
            "email":    request.form['email'],
            "password": request.form['password']
        }
        try:
            resp = requests.post(f"{USER_SERVICE_URL}/register", json=payload, timeout=5)
            data = resp.json()
            if resp.status_code == 201:
                flash(data['message'], 'success')
                return redirect(url_for('login'))
            else:
                flash(data.get('error', 'Registration failed'), 'danger')
        except requests.exceptions.ConnectionError:
            flash("User Service is unavailable. Please try again.", "danger")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        payload = {
            "username": request.form['username'],
            "password": request.form['password']
        }
        try:
            resp = requests.post(f"{USER_SERVICE_URL}/login", json=payload, timeout=5)
            data = resp.json()
            if resp.status_code == 200:
                session['username'] = request.form['username']
                session['user_id']  = data.get('user_id')
                flash(data['message'], 'success')
                return redirect(url_for('products'))
            else:
                flash(data.get('error', 'Login failed'), 'danger')
        except requests.exceptions.ConnectionError:
            flash("User Service is unavailable. Please try again.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('index'))

@app.route('/products')
def products():
    try:
        resp = requests.get(f"{PRODUCT_SERVICE_URL}/products", timeout=5)
        product_list = resp.json()
    except requests.exceptions.ConnectionError:
        product_list = []
        flash("Product Service is unavailable.", "danger")
    return render_template('products.html', products=product_list, user=session.get('username'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)