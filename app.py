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
                featured=True,
            ),
            "The Quiet Power of Letting Go": dict(
                category="other",
                description="A soft companion for releasing what no longer fits — written for the healing woman.",
                price_naira=10000,
                cover_label="THE QUIET POWER OF LETTING GO",
                delivery_type="link",
                delivery_value="https://selar.com/ogj5169578",
                selar_url="https://selar.com/ogj5169578",
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