# FastAPI Authentication & Dynamic RBAC System

A **production-ready FastAPI backend** implementing **secure authentication**, **JWT token invalidation**, and a **dynamic Role-Based Access Control (RBAC)** system using **PostgreSQL**.

This project follows clean architecture principles and is suitable for real-world, scalable applications.

---

## 🚀 Features

### 🔐 Authentication
- User signup & login
- Password hashing with bcrypt
- Email verification support
- JWT access tokens
- **Token invalidation using `token_version`**
- Automatic token revocation on:
  - Re-login
  - Role change
  - Permission change

### 🛡️ Authorization (RBAC)
- Fully dynamic roles (admin, user, editor, etc.)
- Fully dynamic permissions (`rbac:manage`, `user:create`, etc.)
- Many-to-many relationships:
  - Users ↔ Roles
  - Roles ↔ Permissions
- Permission-based route protection
- Admin-only RBAC management APIs

### 🧱 Architecture
- Router → Service → Repository pattern
- ORM models separated from response schemas
- Dependency-based authentication & authorization
- Secure and limited API responses

---

## 🧩 Tech Stack

- FastAPI
- SQLAlchemy (sync)
- PostgreSQL
- Alembic
- Pydantic
- JWT (python-jose)
- Uvicorn

---

## 📁 Project Structure

```
app/
├── core/                   # App configuration
├── db/
│   ├── database.py         # SQLAlchemy Base & engine
|   ├── schemas/            # Pydantic request/response models
│   └── models/             # ORM models (User, Role, Permission)
├── services/               # Business logic
├── routers/                # API routes
├── utils/
│   ├── auth_handler.py
│   ├── protectRoute.py     # get_current_user (returns ORM User)
│   ├── permission_dependency.py
│   └── permission_resolver.py
└── main.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/manjeetbargoti/fastapi-auth.git
cd fastapi-auth
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🗄️ PostgreSQL Configuration

Create database:
```sql
CREATE DATABASE fastapi_auth;
```

Create a `.env` file:
```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/fastapi_auth

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

FRONTEND_URL=http://localhost:8000
```

---

## 🧬 Database Migrations

```bash
alembic upgrade head
```

RBAC tables included:
- `roles`
- `permissions`
- `user_roles`
- `role_permissions`

---

## 🔑 Authentication Flow

1. **Signup**
   - User created
   - Default role assigned
2. **Login**
   - JWT issued
   - `token_version` embedded
3. **Re-login / RBAC update**
   - `token_version` increments
   - Old tokens revoked instantly
4. **Authorization**
   - Permissions resolved dynamically from DB

---

## 🛡️ Route Protection Examples

### Auth-only route
```python
@router.get("/me", response_model=GetCurrentUserOutput)
def me(user = Depends(get_current_user)):
    return user
```

### Permission-protected route
```python
@router.delete("/users/{id}")
def delete_user(
    _ = Depends(require_permissions("user:delete"))
):
    ...
```

---

## 🔒 Security Highlights

- Passwords never exposed
- `token_version` never exposed
- ORM objects used internally, schemas used for output
- RBAC checks always database-backed
- Public routes (`login`, `signup`) excluded from RBAC

---

## 🧪 Core API Endpoints

| Method | Endpoint | Description |
|------|--------|-------------|
| POST | /auth/signup | Register user |
| POST | /auth/login | Login |
| GET  | /me | Current user (safe response) |
| POST | /admin/roles | Create role |
| POST | /admin/permissions | Create permission |
| POST | /admin/users/{user_id}/roles/{role_id} | Assign role |

---

## 🛣️ Roadmap

- Refresh token rotation
- Permission caching (Redis)
- RBAC audit logs
- Super-admin bootstrap
- Docker & docker-compose
- Async SQLAlchemy

---

## 📄 License

MIT License

---

## 👤 Author

**Manjeet Bargoti**  
GitHub: https://github.com/manjeetbargoti
