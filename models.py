from extensions import db

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