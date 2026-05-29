# product-service/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    price       = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()
    # Seed some products if table is empty
    if Product.query.count() == 0:
        seeds = [
            Product(name="Laptop Pro",      description="High-performance laptop", price=999.99, stock=10),
            Product(name="Wireless Mouse",  description="Ergonomic wireless mouse", price=29.99,  stock=50),
            Product(name="Mechanical Keyboard", description="RGB mechanical keyboard", price=79.99, stock=30),
            Product(name="USB-C Hub",       description="7-in-1 USB-C hub",        price=49.99,  stock=25),
        ]
        db.session.bulk_save_objects(seeds)
        db.session.commit()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Product Service is healthy ✅"})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id, "name": p.name,
        "description": p.description,
        "price": p.price, "stock": p.stock
    } for p in products])

@app.route('/products/<int:pid>', methods=['GET'])
def get_product(pid):
    p = Product.query.get_or_404(pid)
    return jsonify({"id": p.id, "name": p.name, "description": p.description,
                    "price": p.price, "stock": p.stock})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({"error": "name and price are required"}), 400
    p = Product(name=data['name'], description=data.get('description', ''),
                price=data['price'], stock=data.get('stock', 0))
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Product added!", "id": p.id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)