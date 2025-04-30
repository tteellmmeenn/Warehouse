# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    model_no = db.Column(db.String(100))
    price = db.Column(db.Float)
    warranty = db.Column(db.String(100))

    def __repr__(self):
        return f"<Item {self.name}>"