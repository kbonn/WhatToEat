from dotenv import load_dotenv
load_dotenv() # Load variables from .env file into environment

from flask import Flask, render_template, request, redirect, url_for
from config import Config # Import your Config class
from extensions import db, migrate # Import extensions
from models import Restaurant # Import Restaurant model

# Create the Flask app instance
app = Flask(__name__, instance_relative_config=True) # instance_relative_config=True helps find config in instance folder if needed
app.config.from_object(Config) # Load configuration from Config object

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

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