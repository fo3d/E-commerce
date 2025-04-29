
import os

# Create 'templates' folder if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')
# Create home.html if it doesn't exist
home_html_path = os.path.join('templates', 'home.html')
if not os.path.exists(home_html_path):
    with open(home_html_path, 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Product List</title>
</head>
<body>
    <h1>Available Products</h1>
    <ul>
        {% for product in products %}
            <li>{{ product.name }} - ${{ product.price }}</li>
        {% endfor %}
    </ul>
</body>
</html>''')

from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99, "description": "High performance laptop."},
        {"id": 2, "name": "Smartphone", "price": 499.99, "description": "Latest Android phone."},
        {"id": 3, "name": "Headphones", "price": 89.99, "description": "Noise-cancelling headphones."},
        {"id": 4, "name": "Monitor", "price": 199.99, "description": "Full HD 24-inch display."},
        {"id": 5, "name": "Keyboard", "price": 29.99, "description": "Mechanical RGB keyboard."},
        {"id": 6, "name": "Mouse", "price": 19.99, "description": "Ergonomic wireless mouse."},
        {"id": 7, "name": "Tablet", "price": 299.99, "description": "10-inch Android tablet."},
        {"id": 8, "name": "Smartwatch", "price": 149.99, "description": "Fitness tracking smartwatch."},
        {"id": 9, "name": "Bluetooth Speaker", "price": 59.99, "description": "Portable speaker with bass."},
        {"id": 10, "name": "Gaming Chair", "price": 189.99, "description": "Comfortable gaming chair."},
        {"id": 11, "name": "Webcam", "price": 49.99, "description": "HD webcam for video calls."},
        {"id": 12, "name": "Microphone", "price": 79.99, "description": "USB condenser mic."},
        {"id": 13, "name": "External HDD", "price": 99.99, "description": "1TB portable hard drive."},
        {"id": 14, "name": "Power Bank", "price": 39.99, "description": "10,000 mAh fast-charging."},
        {"id": 15, "name": "Router", "price": 59.99, "description": "Dual-band WiFi router."},
        {"id": 16, "name": "Printer", "price": 129.99, "description": "Wireless inkjet printer."},
        {"id": 17, "name": "SSD", "price": 89.99, "description": "500GB internal SSD."},
        {"id": 18, "name": "Graphics Card", "price": 399.99, "description": "Mid-range GPU."},
        {"id": 19, "name": "Drone", "price": 249.99, "description": "Quadcopter with 4K camera."},
        {"id": 20, "name": "VR Headset", "price": 349.99, "description": "Immersive virtual reality experience."}
    ]
    return render_template('home.html', products=products)

users = {
    'user@example.com': {
        'id': 1,
        'email': 'user@example.com',
        'username': 'JohnDoe',
        'password': '123456'  # In real apps, use hashed passwords
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.get(email)

        if user and password == user['password']:  # use check_password_hash(user['password'], password) if hashed
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')
# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

# Routes


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    new_item = Cart(user_id=session['user_id'], product_id=product_id)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    items = Cart.query.filter_by(user_id=session['user_id']).all()
    products = [Product.query.get(item.product_id) for item in items]
    return render_template('cart.html', products=products)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)

