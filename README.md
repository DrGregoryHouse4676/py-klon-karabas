# py-klon-karabas 🎭 TheatreBox API

**TheatreBox** is a Karabas educational clone built on **Django + DRF**.
The goal is online theater seat booking: actors, genres, performances, halls, sessions, reservations and tickets.
---

## 🚀 Technology stack
- Python 3.11+
- Django 5.x
- Django REST Framework
- DRF Spectacular (OpenAPI docs)
- PostgreSQL (through Docker)
- Pytest 
- Docker + docker-compose

---

## ⚡ Quick Start (Local)

### 1. Clone repository
```bash
git clone <repo-url>
cd py-klon-karabas
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 2. Configure .env
Minimal example:
```
DJANGO_SECRET_KEY=dev-secret
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*

POSTGRES_DB=theatre
POSTGRES_USER=theatre
POSTGRES_PASSWORD=theatre
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
### 3. Migrations + superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```
### 4. Starting the server
```
python manage.py runserver
API: http://127.0.0.1:8000/api/
admin: http://127.0.0.1:8000/admin/
Docs: http://127.0.0.1:8000/api/docs/
```
### 🐳 Running via Docker
```
docker compose up --build
web application: http://127.0.0.1:8000
database: localhost:5432
```

📂 Project structure
```
theatrebox/         # Settings Django (urls, settings)
theatre/            # Basic business logic
  ├── models.py
  ├── serializers.py
  ├── views.py
  ├── urls.py
  └── services/
templates/          # Custom HTML templates (admin)
static/             # Static files (CSS, JS)
tests/              # Pytest-tests
```
### 🔐 Authentication
```
Used JWT (SimpleJWT).
POST /api/token/ — get access + refresh
POST /api/token/refresh/ — refresh access
Example:
POST /api/token/
{
  "username": "admin",
  "password": "password123"
}
```

# 👨‍💻 Автор: Lev Ivanov