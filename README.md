# FastAPI Authentication & Dynamic RBAC System

A **production-ready FastAPI backend** implementing **secure authentication** and a **dynamic Role-Based Access Control (RBAC)** system using **PostgreSQL**, **SQLAlchemy (Async)**, and **Alembic**.

This project follows clean architecture principles and is designed for real-world, scalable applications.

---

## 🚀 Features

### 🔐 Authentication
- User registration & login
- Password hashing with `bcrypt`
- JWT access tokens
- Token invalidation using `token_version`
- Email configuration support
- Secure dependency-based route protection

### 🛂 Authorization (RBAC)
- Dynamic roles & permissions
- Database-driven permission system
- Route-level permission enforcement
- Reusable permission dependencies
- Fine-grained access control for APIs

### 🧱 Architecture
- Modular, clean structure
- Async SQLAlchemy
- Alembic migrations
- Environment-based configuration
- CLI utilities for seeding data

---

## 📁 Project Structure

```
fast_api_auth/
├── main.py
├── requirements.txt
├── .env
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── create_users_table.py
│       └── create_rbac_table.py
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── services/
│   ├── utils/
│   │   ├── init_db.py
│   │   ├── protectRoute.py
│   │   ├── permission_dependency.py
│   │   └── permission_resolver.py
│   └── cli/
│       └── seed.py
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/fast-api-auth.git
cd fast-api-auth
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create a `.env` file in the project root with the following variables.
**Do not commit real secrets to version control.**

```env
FRONTEND_URL=

DATABASE_URL=

JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
EMAIL_TOKEN_EXP_MIN=

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_SERVER=
MAIL_PORT=
MAIL_STARTTLS=
MAIL_SSL_TLS=
USE_CREDENTIALS=
VALIDATE_CERTS=

SEED_ADMIN_EMAIL=
SEED_ADMIN_PASSWORD=
SEED_ADMIN_FIRST_NAME=
SEED_ADMIN_LAST_NAME=

SEED_USER_EMAIL=
SEED_USER_PASSWORD=
SEED_USER_FIRST_NAME=
SEED_USER_LAST_NAME=
```

---

## 🗄️ Database & Migrations

Run migrations:

```bash
alembic upgrade head
```

---

## 🌱 Seed Initial Data

```bash
python -m app.cli.seed
```

---

## ▶️ Run Application

```bash
uvicorn main:app --reload
```

- API Base URL: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`
- Health Check: `GET /health`

---

## 🔐 Protecting Routes with Permissions

```python
from app.utils.permission_dependency import PermissionDependency

@router.get(
    "/admin/users",
    dependencies=[PermissionDependency("user.read")]
)
async def list_users():
    return {"message": "Only authorized users can access this"}
```

---

## 📄 License

MIT License

---

## 👤 Author

**Manjeet Bargoti**  
GitHub: https://github.com/manjeetbargoti
