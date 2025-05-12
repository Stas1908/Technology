from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Лабораторна №1 через Render виконана успішно!"