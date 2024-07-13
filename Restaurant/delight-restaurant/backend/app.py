import datetime
from flask import Flask, request, jsonify, logging, abort, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from functools import wraps
import json
from werkzeug.exceptions import Forbidden
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import session
from datetime import datetime
from sqlalchemy import Text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/Delight Restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['JWT_SECRET_KEY'] = 'replace_this_with_your_secret_key'  # Change this to a secure random key
CORS(app)  # Enable CORS for all routes
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, username, password, role, email):
        self.username = username
        self.password = password
        self.role = role
        self.email = email

# Utility function to check admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user or current_user['role'] != 'admin':
            return jsonify({'message': 'Access forbidden: Admins only'}), 403
        return f(*args, **kwargs)
    return decorated_function

class MenuItem(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    availability = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'availability': self.availability
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'order_date' : self.order_date,
            'order_items' : self.order_items
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_total = db.Column(db.Numeric(10, 2), nullable=False)  # Ensure item_total is included

    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'item_total': self.item_total
        }
        
# Route to register a new user
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')

    if not all([username, password, role, email]):
        return jsonify({'message': 'All fields are required!'}), 400

    # hashed_password = password # generate_password_hash(password, method='sha256')
    new_user = User(username=username, password= password, role=role, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

# Route to login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username,password=password).first()

    #if user and check_password_hash(user.password, password):
    if user:
        return jsonify({'message': 'Login successful', 'role': user.role})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Route to get all menu items
@app.route('/api/menu', methods=['GET'])
def get_menu():
    menu_items = MenuItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': str(item.price),
        'availability': item.availability
    } for item in menu_items])

@app.route('/api/user/menu', methods=['GET'])
def get_userSmenu():
    menu_items = MenuItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': str(item.price),
        'availability': item.availability
    } for item in menu_items])
# Fetch all menu items
@app.route('/api/admin/menu', methods=['GET'])
def get_adminmenu_items():
    try:
        menu_items = MenuItem.query.all()
        serialized_menu = [item.serialize() for item in menu_items]
        return jsonify(serialized_menu), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Add a new menu item
@app.route('/api/admin/menu', methods=['POST'])
def add_menu_item():
    try:
        new_item_data = request.json
        new_item = MenuItem(
            name=new_item_data['name'],
            description=new_item_data.get('description', ''),
            price=float(new_item_data['price']),
            availability=new_item_data.get('availability', True)
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Menu item added successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Menu item already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing menu item
@app.route('/api/admin/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    try:
        item = MenuItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Menu item not found'}), 404

        data = request.json
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.price = float(data.get('price', item.price))
        item.availability = data.get('availability', item.availability)  # Ensure the key is 'availability'

        db.session.commit()
        return jsonify({'message': 'Menu item updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a menu item
@app.route('/api/admin/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        item = MenuItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Menu item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Menu item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
