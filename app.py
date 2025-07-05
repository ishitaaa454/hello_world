from flask import Flask, render_template, send_from_directory
from backend.api import api_bp
import os

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True) 