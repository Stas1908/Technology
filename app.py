from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    return "Лабораторна №2. CRUD-сервер працює на Render!"

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(read_data())

@app.route('/items', methods=['POST'])
def create_item():
    data = read_data()
    item = request.json
    data.append(item)
    write_data(data)
    return jsonify(item), 201

@app.route('/items/<int:index>', methods=['PUT'])
def update_item(index):
    data = read_data()
    if 0 <= index < len(data):
        data[index] = request.json
        write_data(data)
        return jsonify(data[index])
    return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    data = read_data()
    if 0 <= index < len(data):
        item = data.pop(index)
        write_data(data)
        return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
