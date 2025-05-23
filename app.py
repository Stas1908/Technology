from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Встановлюємо рядок підключення до БД через змінну оточення або прямо тут:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://lab4db_6dwg_user:Ga9Q7yWEFMdPn8f3jTA4VNGZNYs2HhUH@dpg-d0o2htvdiees739jl230-a.oregon-postgres.render.com/lab4db_6dwg')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Створюємо модель (таблицю) для збереження елементів
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)

@app.route('/')
def home():
    items = Item.query.order_by(Item.id).all()  # Сортування за id
    items_list = "<ul>"
    for i in items:
        items_list += f"<li>{i.id}: {i.data}</li>"
    items_list += "</ul>"
    return f"<h1>Список елементів</h1>{items_list}"

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.order_by(Item.id).all()  # Сортування за id
    return jsonify([{'id': i.id, 'data': i.data} for i in items])

@app.route('/items', methods=['POST'])
def create_item():
    item_data = request.json.get('data')
    if not item_data:
        return jsonify({'error': 'No data provided'}), 400
    item = Item(data=item_data)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id, 'data': item.data}), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    item_data = request.json.get('data')
    if not item_data:
        return jsonify({'error': 'No data provided'}), 400
    item.data = item_data
    db.session.commit()
    return jsonify({'id': item.id, 'data': item.data})

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'result': 'Item deleted'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
