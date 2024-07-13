    from datetime import datetime, date, time
    from flask import Flask, request, jsonify, logging, abort, g
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.exc import IntegrityError
    from flask_cors import CORS
    from functools import wraps
    import json
    from sqlalchemy.exc import SQLAlchemyError
    from werkzeug.exceptions import Forbidden
    from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
    from flask import session
    from sqlalchemy import JSON
    import logging

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/Delight Restaurant'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['JWT_SECRET_KEY'] = 'replace_this_with_your_secret_key'  # Change this to a secure random key
    CORS(app)  # Enable CORS for all routes

    db = SQLAlchemy(app)
    jwt = JWTManager(app)

    logging.basicConfig(level=logging.DEBUG)

    # Define User model
    class User(db.Model):
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        role = db.Column(db.String(20), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

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

    class User(db.Model):
        user_id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)
        full_name = db.Column(db.String(100))
        user_type = db.Column(db.String(20), nullable=False)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')
        email = data.get('email')

        if not all([username, password, user_type, email]):
            return jsonify({'message': 'All fields are required!'}), 400

        new_user = User(username=username, password=password, user_type=user_type, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Registration failed: {str(e)}'}), 500

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
    def get_menu_items():
        try:
            menu_items = Menu.query.all()
            serialized_menu = [item.serialize() for item in menu_items]
            return jsonify(serialized_menu), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Route to add a new menu item (Admin only)
    @app.route('/api/menu', methods=['POST'])
    @jwt_required()
    @admin_required
    def add_menu_item():
        try:
            new_item_data = request.json
            if 'name' not in new_item_data or not new_item_data['name']:
                return jsonify({'message': 'Name is required'}), 400
            if 'price' not in new_item_data or not isinstance(new_item_data['price'], (int, float)):
                return jsonify({'message': 'Price is required and must be a number'}), 400

            new_item = Menu(
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

    # Route to update an existing menu item (Admin only)
    @app.route('/api/menu/<int:item_id>', methods=['PUT'])
    @jwt_required()
    @admin_required
    def update_menu_item(item_id):
        try:
            item = Menu.query.get(item_id)
            if not item:
                return jsonify({'error': 'Menu item not found'}), 404

            data = request.json
            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.price = float(data.get('price', item.price))
            item.availability = data.get('availability', item.availability)

            db.session.commit()
            return jsonify({'message': 'Menu item updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Route to delete a menu item (Admin only)
    @app.route('/api/menu/<int:item_id>', methods=['DELETE'])
    @jwt_required()
    @admin_required
    def delete_menu_item(item_id):
        try:
            item = Menu.query.get(item_id)
            if not item:
                return jsonify({'error': 'Menu item not found'}), 404

            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Menu item deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/reservations', methods=['GET'])
    def get_all_reservations():
        try:
            reservations = Reservation.query.all()
            serialized_reservations = [reservation.serialize() for reservation in reservations]
            return jsonify(serialized_reservations), 200
        except Exception as e:
            print(f"Error fetching reservations: {e}")
            return jsonify({'error': 'Failed to fetch reservations'}), 500
        
    # Define the MenuItem model
    class Menu(db.Model):
        __tablename__ = 'menu'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text)
        price = db.Column(db.Float, nullable=False)
        availability = db.Column(db.Boolean, default=True)

        def serialize(self):
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': float(self.price),
                'availability': self.availability
            }

    class Customer(db.Model):
        __tablename__ = 'customers'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique = True, nullable=False)
        contact_details = db.Column(db.String(255))
        order_history = db.Column(db.JSON)  # Assuming order_history is stored as JSON data

        def __repr__(self):
            return f'<Customer {self.name}>'
        
    # Define the Order model
    class Order(db.Model):
        __tablename__ = 'orders'

        id = db.Column(db.Integer, primary_key=True)
        order_details = db.Column(JSON, nullable=False)
        timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        def __repr__(self):
            return f'<Order {self.id}>'

        def serialize(self):
            return {
                'id': self.id,
                'order_details': self.order_details,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }

                    
    class Reservation(db.Model):
        __tablename__ = 'reservations'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        date = db.Column(db.Date, nullable=False)
        time = db.Column(db.Time, nullable=False)
        people = db.Column(db.Integer, nullable=False)

        def serialize(self):
            return {
                'id': self.id,
                'name': self.name,
                'date': self.date.isoformat(),
                'time': self.time.isoformat(),
                'people': self.people,
            }
            
    @app.route('/api/reservations', methods=['POST'])
    def reserve_table():
        data = request.json
        name = data.get('name')
        date_str = data.get('date')
        time_str = data.get('time')
        people = data.get('numberOfGuests')

        if not name or not date_str or not time_str or not people:
            return jsonify({'error': 'Missing data'}), 400

        try:
            # Parse date string into datetime object
            reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Parse time string with or without seconds into time object
            if len(time_str) == 5:
                reservation_time = datetime.strptime(time_str, '%H:%M').time()
            else:
                reservation_time = datetime.strptime(time_str, '%H:%M:%S').time()

            reservation = Reservation(
                name=name,
                date=reservation_date,
                time=reservation_time,
                people=int(people),  # Ensure people is an integer
            )
            db.session.add(reservation)
            db.session.commit()
            return jsonify({'message': 'Table reserved successfully!'}), 201
        except ValueError as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Invalid date or time format'}), 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
    # Route to place an order
    @app.route('/api/orders', methods=['POST'])
    def place_order():
        data = request.json
        order_details = data.get('items', [])  # Check if 'items' key is correctly accessed

        try:
            new_order = Order(order_details=order_details)
            db.session.add(new_order)
            db.session.commit()
            return jsonify({'message': 'Order placed successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    @app.route('/api/orders', methods=['GET'])
    def get_orders():
        try:
            orders = Order.query.all()
            serialized_orders = [{
                'id': order.id,
                'order_details': order.order_details,
                'timestamp': order.timestamp
            } for order in orders]
            return jsonify(serialized_orders), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/orders', methods=['GET'])
    def get_all_orders():
        try:
            orders = Order.query.all()
            return jsonify([order.serialize() for order in orders]), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Failed to fetch orders'}), 500

    @app.route('/api/customers', methods=['GET'])
    def get_customers():
        try:
            customers = Customer.query.all()
            serialized_customers = [{
                'id': customer.id,
                'name': customer.name,
                'contact_details': customer.contact_details,
                'order_history': customer.order_history
            } for customer in customers]
            return jsonify(serialized_customers), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Route for logging out
    @app.route('/api/logout', methods=['POST'])
    def logout():
        session.pop('username', None)
        session.pop('role', None)
        return jsonify({'message': 'Logged out successfully'}), 200

    # CORS handling and menu item management routes
    # Routes for admin operations
    @app.route('/api/admin/menu', methods=['GET'])
    def get_adminmenu_items():
        try:
            menu_items = Menu.query.all()
            return jsonify([item.serialize() for item in menu_items])
        except SQLAlchemyError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/menu/<int:item_id>', methods=['GET'])
    def get_adminmenu_item(item_id):
        try:
            menu_item = Menu.query.get(item_id)
            if menu_item:
                return jsonify(menu_item.serialize())
            else:
                return jsonify({'error': 'Menu item not found'}), 404
        except SQLAlchemyError as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/menu', methods=['POST'])
    def add_adminmenu_item():
        try:
            data = request.get_json()

            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            availability = data.get('available', True)  # Default to True if 'available' is not present

            if not all([name, description, price]):
                logging.error(f"Missing required fields: {data}")
                return jsonify({"error": "Missing required fields"}), 400

            new_item = Menu(
                name=name,
                description=description,
                price=price,
                availability=availability
            )

            db.session.add(new_item)
            db.session.commit()

            return jsonify({"message": "Menu item added successfully"}), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemyError: {str(e)}")
            return jsonify({"error": str(e)}), 500

        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/admin/menu/<int:item_id>', methods=['PUT'])
    def update_adminmenu_item(item_id):
        try:
            data = request.get_json()
            logging.debug(f"Received data for update: {data}")

            item_to_update = Menu.query.get(item_id)
            if not item_to_update:
                logging.error(f"Menu item with id {item_id} not found.")
                return jsonify({"error": "Menu item not found"}), 404

            # Check for missing fields and log warnings
            if 'name' not in data:
                logging.warning("Missing 'name' field in update data")
            if 'description' not in data:
                logging.warning("Missing 'description' field in update data")
            if 'price' not in data:
                logging.warning("Missing 'price' field in update data")
            if 'available' not in data:
                logging.warning("Missing 'available' field in update data")

            item_to_update.name = data.get('name', item_to_update.name)
            item_to_update.description = data.get('description', item_to_update.description)
            item_to_update.price = data.get('price', item_to_update.price)
            item_to_update.availability = data.get('available', item_to_update.availability)

            db.session.commit()
            return jsonify({"message": "Menu item updated successfully"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"SQLAlchemyError: {str(e)}")
            return jsonify({"error": str(e)}), 500

        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/admin/menu/<int:item_id>', methods=['DELETE'])
    def delete_adminmenu_item(item_id):
        try:
            item_to_delete = Menu.query.get(item_id)
            if not item_to_delete:
                return jsonify({'error': 'Menu item not found'}), 404
            db.session.delete(item_to_delete)
            db.session.commit()
            return jsonify({'message': 'Menu item deleted successfully'})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/admin/menu', methods=['GET'])
    def get_menu():
        try:
            menu_items = Menu.query.all()
            serialized_menu = [{
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "available": item.availability
            } for item in menu_items]
            return jsonify(serialized_menu), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def __repr__(self):
            return f'<Menu {self.name}>'

    # API route to add a new menu item
    # Run the Flask app
    if __name__ == '__main__':
        app.run(debug=True)
