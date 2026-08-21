import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Order, Subscriber

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///shop.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    def _sync_products():
        """Keeps the live product catalog in sync with this list every time the app starts.
        Edit prices/products here, redeploy, and the storefront updates automatically —
        including removing anything no longer in this list."""
        catalog = {
            "Letters to the Soft Woman": dict(
                category="other",
                description="Gentle letters for women in the middle of becoming — for the quiet, tender seasons.",
                price_naira=5000,
                cover_label="LETTERS TO THE SOFT WOMAN",
                delivery_type="link",
                delivery_value="https://selar.com/ogj5169578",
                selar_url="https://selar.com/ogj5169578",
                featured=False,
            ),
            "The Quiet Power of Letting Go": dict(
                category="other",
                description="A soft companion for releasing what no longer fits — written for the healing woman.",
                price_naira=10000,
                cover_label="THE QUIET POWER OF LETTING GO",
                delivery_type="link",
                delivery_value="https://selar.com/u7vi587959",
                selar_url="https://selar.com/u7vi587959",
                featured=False,
            ),
            "Wink Makes a Friend — A Bubblewink Meadow Storybook": dict(
                category="kids",
                description="An illustrated storybook (PDF) about Wink, a gentle little creature learning what it means to make a friend.",
                price_naira=2000,
                cover_label="WINK MAKES A FRIEND",
                delivery_type="link",
                delivery_value="https://selar.com/923p247857",
                selar_url="https://selar.com/923p247857",
                featured=True,
            ),
            "Wink & Pip's Pebble Hunt Activity Pack": dict(
                category="kids",
                description="A printable activity pack (PDF) — pebble hunts, puzzles, and coloring pages from Bubblewink Meadow.",
                price_naira=2000,
                cover_label="WINK & PIP'S PEBBLE HUNT",
                delivery_type="link",
                delivery_value="https://selar.com/648pl59639",
                selar_url="https://selar.com/648pl59639",
                featured=False,
            ),
        }

        # remove anything not in the current catalog (e.g. unpublished books)
        for p in Product.query.all():
            if p.name not in catalog:
                db.session.delete(p)

        # add new products, update existing ones (so price/description edits take effect)
        for name, data in catalog.items():
            existing = Product.query.filter_by(name=name).first()
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                db.session.add(Product(name=name, **data))

        db.session.commit()

    with app.app_context():
        db.create_all()
        _sync_products()

    # ---------- storefront ----------
    @app.route("/")
    def home():
        products = Product.query.filter_by(active=True).order_by(Product.featured.desc(), Product.created_at.desc()).all()
        featured = next((p for p in products if p.featured), None)
        return render_template("index.html", products=products, featured=featured)

    @app.route("/product/<product_id>")
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        return render_template("product.html", product=product)

    # ---------- newsletter ----------
    @app.route("/subscribe", methods=["POST"])
    def subscribe():
        email = request.form.get("email", "").strip().lower()
        if not email or "@" not in email:
            flash("Please enter a valid email.")
            return redirect(url_for("home") + "#newsletter")

        existing = Subscriber.query.filter_by(email=email).first()
        if not existing:
            db.session.add(Subscriber(email=email))
            db.session.commit()

        flash("You're subscribed — thank you!")
        return redirect(url_for("home") + "#newsletter")

    @app.route("/admin/subscribers")
    def admin_subscribers():
        subs = Subscriber.query.order_by(Subscriber.created_at.desc()).all()
        return render_template("admin_subscribers.html", subscribers=subs)

    # ---------- simple admin: add products ----------
    @app.route("/admin/products", methods=["GET", "POST"])
    def admin_products():
        if request.method == "POST":
            p = Product(
                name=request.form["name"],
                category=request.form["category"],
                description=request.form["description"],
                price_naira=int(request.form["price_naira"]),
                cover_label=request.form.get("cover_label", ""),
                delivery_type=request.form.get("delivery_type", "link"),
                delivery_value=request.form.get("delivery_value", ""),
                selar_url=request.form.get("selar_url", ""),
                featured=bool(request.form.get("featured")),
            )
            db.session.add(p)
            db.session.commit()
            flash(f"Added {p.name}")
            return redirect(url_for("admin_products"))

        products = Product.query.order_by(Product.created_at.desc()).all()
        return render_template("admin.html", products=products)

    @app.route("/admin/products/<product_id>/delete", methods=["POST"])
    def admin_delete_product(product_id):
        p = Product.query.get_or_404(product_id)
        db.session.delete(p)
        db.session.commit()
        return redirect(url_for("admin_products"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)