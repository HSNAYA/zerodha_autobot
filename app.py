from flask import Flask, render_template, request, redirect, session, jsonify
import os
from kite_auth import get_kite, place_order
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('dashboard.html')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == os.getenv('DASH_USERNAME') and request.form['password'] == os.getenv('DASH_PASSWORD'):
            session['logged_in'] = True
            return redirect('/')
    return render_template('login.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    return jsonify({'status': 'received', 'data': data})

@app.route('/healthz')
def health():
    return jsonify({'status': 'alive'})

if __name__ == '__main__':
    app.run(debug=True)