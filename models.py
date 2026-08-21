from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


def gen_id():
    return uuid.uuid4().hex[:12]


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.String(12), primary_key=True, default=gen_id)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)   # book, dental, other
    description = db.Column(db.Text, nullable=False)
    price_naira = db.Column(db.Integer, nullable=False)    # stored in naira (whole number)
    cover_label = db.Column(db.String(40), default="")     # short text shown on the cover block
    delivery_type = db.Column(db.String(20), default="link")  # link | file | message
    delivery_value = db.Column(db.Text, default="")        # URL, file path, or pickup message
    selar_url = db.Column(db.Text, default="")             # direct link to this product's Selar checkout page
    featured = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def price_kobo(self):
        return self.price_naira * 100


class Subscriber(db.Model):
    __tablename__ = "subscribers"

    id = db.Column(db.String(12), primary_key=True, default=gen_id)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.String(12), primary_key=True, default=gen_id)
    reference = db.Column(db.String(64), unique=True, nullable=False)
    product_id = db.Column(db.String(12), db.ForeignKey("products.id"), nullable=False)
    buyer_name = db.Column(db.String(120), nullable=False)
    buyer_email = db.Column(db.String(120), nullable=False)
    amount_naira = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="pending")   # pending | paid | failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)

    product = db.relationship("Product", backref="orders")