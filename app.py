import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Order

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///shop.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    def _auto_seed_if_empty():
        if Product.query.count() > 0:
            return
        starter_products = [
            dict(
                name="AI Unlocked: The Complete Guide to Understanding, Using, and Thriving with Artificial Intelligence",
                category="book",
                description="A full, plain-language guide to AI — for anyone who wants to actually understand and use it, not just hear about it.",
                price_naira=5000,
                cover_label="AI UNLOCKED",
                delivery_type="link",
                delivery_value="https://selar.com/ogj5169578",
                selar_url="https://selar.com/ogj5169578",
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
                selar_url="https://selar.com/ogj5169578",
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
                selar_url="https://selar.com/ogj5169578",
                featured=False,
            ),
        ]
        for data in starter_products:
            db.session.add(Product(**data))
        db.session.commit()

    with app.app_context():
        db.create_all()
        _auto_seed_if_empty()

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
