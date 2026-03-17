# Global Paint

Python/Flask app with Admin (Render) & Staff (Contabo) sites sharing Supabase PostgreSQL via SQLAlchemy models.

## Folder Structure
```
global-paint/
├── admin_site/     # Full CRUD admin
├── staff_site/     # Ops dashboard
├── shared/         # DB models
├── .env.example
└── README.md
```

## Quick Start

1. Copy `.env.example` to `.env`, add Supabase DATABASE_URL, SECRET_KEY.

2. Admin:
```
cd admin_site
pip install -r requirements.txt
flask db init
flask db migrate -m "initial"
flask db upgrade
FLASK_APP=app flask run
```

3. Staff:
```
cd staff_site
pip install -r requirements.txt
FLASK_APP=app flask run
```

## Deployment
- Admin: Render (Python), set DATABASE_URL, SECRET_KEY env vars.
- Staff: Contabo VPS (gunicorn or uvicorn).

## Models
- User (admin/staff login, inventory owner)
- InventoryItem
- GlobalSetting

Admin: /login -> dashboard -> users/inventory/settings lists.
Staff: /login -> dashboard (own items), /log.

Extend CRUD, add WTForms, security (hash passwords on create).
