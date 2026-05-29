# user-service/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "User Service is healthy ✅"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409

    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User '{data['username']}' registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password, data.get('password', '')):
        return jsonify({"message": f"Welcome back, {user.username}!", "user_id": user.id}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)



## user-service/app.py
# from flask import Flask, request, jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
# from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
# import os

# app = Flask(__name__)

# # ─────────────────────────────────────────────
# # Azure Cosmos DB (MongoDB API) Connection
# # ─────────────────────────────────────────────
# COSMOS_CONNECTION_STRING = os.getenv(
#     "COSMOS_CONNECTION_STRING",
#     "mongodb://<your-account>:<your-key>@<your-account>.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@<your-account>@"
# )

# try:
#     client     = MongoClient(COSMOS_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
#     db         = client["shopcart"]          # database name
#     users_col  = db["users"]                 # collection name

#     # Ensure unique index on username and email
#     users_col.create_index("username", unique=True)
#     users_col.create_index("email",    unique=True)

#     print("✅ Connected to Azure Cosmos DB (MongoDB API)")
# except ServerSelectionTimeoutError as e:
#     print(f"❌ Could not connect to Cosmos DB: {e}")


# # ─────────────────────────────────────────────
# # Routes
# # ─────────────────────────────────────────────

# @app.route('/health', methods=['GET'])
# def health():
#     try:
#         # Ping the database to verify connection is alive
#         client.admin.command('ping')
#         return jsonify({"status": "User Service is healthy ✅", "db": "Cosmos DB connected ✅"}), 200
#     except Exception as e:
#         return jsonify({"status": "Unhealthy ❌", "error": str(e)}), 500


# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()

#     # Validate required fields
#     if not data or not data.get('username') or not data.get('email') or not data.get('password'):
#         return jsonify({"error": "Missing fields: username, email, and password are required"}), 400

#     hashed_pw = generate_password_hash(data['password'])

#     user_doc = {
#         "username": data['username'].strip().lower(),
#         "email":    data['email'].strip().lower(),
#         "password": hashed_pw
#     }

#     try:
#         users_col.insert_one(user_doc)
#         return jsonify({"message": f"User '{data['username']}' registered successfully!"}), 201

#     except DuplicateKeyError:
#         return jsonify({"error": "Username or email already exists"}), 409

#     except Exception as e:
#         return jsonify({"error": f"Database error: {str(e)}"}), 500


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()

#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({"error": "Missing username or password"}), 400

#     try:
#         user = users_col.find_one({"username": data['username'].strip().lower()})

#         if user and check_password_hash(user['password'], data['password']):
#             return jsonify({
#                 "message": f"Welcome back, {user['username']}!",
#                 "user_id": str(user['_id'])   # Cosmos DB uses ObjectId, convert to string
#             }), 200

#         return jsonify({"error": "Invalid credentials"}), 401

#     except Exception as e:
#         return jsonify({"error": f"Database error: {str(e)}"}), 500


# @app.route('/users', methods=['GET'])
# def list_users():
#     try:
#         users = users_col.find({}, {"_id": 0, "password": 0})  # exclude _id and password
#         return jsonify(list(users)), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)