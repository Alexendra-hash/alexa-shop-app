"""
Run once after the database is created to load your starting products.
Usage: python seed.py

Edit selar_url below for each product to the direct link to that product's
own Selar checkout page (find this in your Selar dashboard under each product).
"""
from app import create_app
from models import db, Product

app = create_app()

PRODUCTS = [
    dict(
        name="AI Unlocked: The Complete Guide to Understanding, Using, and Thriving with Artificial Intelligence",
        category="book",
        description="A full, plain-language guide to AI — for anyone who wants to actually understand and use it, not just hear about it.",
        price_naira=5000,
        cover_label="AI UNLOCKED",
        delivery_type="link",
        delivery_value="https://selar.com/ogj5169578",
        selar_url="https://selar.com/ogj5169578",   # replace with this book's specific Selar product link
        featured=True,
    ),
    dict(
        name="Letters to the Soft Woman",
        category="other",
        description="Gentle letters for women in the middle of becoming — for the quiet, tender seasons.",
        price_naira=3000,
        cover_label="LETTERS TO THE SOFT WOMAN",
        delivery_type="link",
        delivery_value="https://selar.com/ogj5169578",
        selar_url="https://selar.com/ogj5169578",   # replace with this book's specific Selar product link
        featured=False,
    ),
    dict(
        name="The Quiet Power of Letting Go",
        category="other",
        description="A soft companion for releasing what no longer fits — written for the healing woman.",
        price_naira=3000,
        cover_label="THE QUIET POWER OF LETTING GO",
        delivery_type="link",
        delivery_value="https://selar.com/ogj5169578",
        selar_url="https://selar.com/ogj5169578",   # replace with this book's specific Selar product link
        featured=False,
    ),
]

with app.app_context():
    for data in PRODUCTS:
        exists = Product.query.filter_by(name=data["name"]).first()
        if not exists:
            db.session.add(Product(**data))
    db.session.commit()
    print(f"Seeded {len(PRODUCTS)} products (skipped any that already existed).")
