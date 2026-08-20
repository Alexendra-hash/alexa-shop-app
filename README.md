# Alexa's Shop

A storefront for digital products (ebooks and dental care resources), built with Flask.
Checkout is handled through Selar — each product's "Buy" button opens that product's
dedicated Selar checkout page.

## Features
- Product catalog with categories (books, dental products, etc.)
- Admin panel at `/admin/products` for adding and removing products without editing code
- Starter products load automatically on first run
- Responsive design

## Tech stack
- Python / Flask
- SQLAlchemy (SQLite for development, Postgres-ready for production)
- Jinja2 templates

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

The app runs at `http://localhost:5000`.

## Deployment

Deployed on Render (Flask requires a persistent server, not static hosting):

1. Connect this repository in Render
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`
4. Set environment variable `SECRET_KEY`

## Project structure
```
app.py              Flask application and routes
models.py            Database models
templates/           HTML templates
static/css/          Stylesheet
requirements.txt     Python dependencies
```

## License
All content, product descriptions, and branding are the property of the repository owner.
