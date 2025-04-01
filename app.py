from dotenv import load_dotenv
load_dotenv() # Load variables from .env file into environment

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate # Import Migrate
from config import Config # Import your Config class

# Create the Flask app instance
app = Flask(__name__, instance_relative_config=True) # instance_relative_config=True helps find config in instance folder if needed
app.config.from_object(Config) # Load configuration from Config object

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db) # Initialize Migrate

# --- Define Database Models (AFTER db is initialized) ---
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cuisine_type = db.Column(db.String(100))
    address = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    rating = db.Column(db.Float)
    price_range = db.Column(db.String(10))  # e.g., "$", "$$", "$$$"
    is_open = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Restaurant {self.name}>'

# --- Routes ---
@app.route('/')
def index():
    try:
        restaurants = Restaurant.query.all()
    except Exception as e:
        print(f"Error querying restaurants: {e}")
        restaurants = []
    return render_template('index.html', title='Welcome', restaurants=restaurants)

@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    if request.method == 'POST':
        name = request.form.get('name')
        cuisine_type = request.form.get('cuisine_type')
        address = request.form.get('address')
        phone = request.form.get('phone')
        rating = float(request.form.get('rating', 0))
        price_range = request.form.get('price_range')
        
        if name:
            try:
                new_restaurant = Restaurant(
                    name=name,
                    cuisine_type=cuisine_type,
                    address=address,
                    phone=phone,
                    rating=rating,
                    price_range=price_range
                )
                db.session.add(new_restaurant)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error adding restaurant: {e}")
        return redirect(url_for('index'))

# Allows running the app directly using 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)