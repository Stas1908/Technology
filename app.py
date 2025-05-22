import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Лабораторна №1 через Render виконана успішно!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # бере порт із змінної середовища, 5000 — дефолт для локального запуску
    app.run(host='0.0.0.0', port=port)
