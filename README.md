# FastAPI Authentication Service (PostgreSQL)

A clean, scalable **authentication backend built with FastAPI and PostgreSQL**, implementing user registration, login, email verification, and JWT-based security.  
Designed using a **router → service → repository** architecture with transaction safety and production best practices.

---

## 🚀 Features

- User signup with password hashing  
- Email verification workflow  
- JWT-based authentication  
- Secure login with verification enforcement  
- PostgreSQL database integration  
- SQLAlchemy ORM  
- Pydantic schemas for validation  
- Background email sending  
- Environment-based configuration  
- Clean, maintainable architecture  

---

## 🧱 Tech Stack

- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- Pydantic  
- JWT (python-jose)  
- FastAPI-Mail  
- Uvicorn  

---

## 📁 Project Structure

```
fastapi-auth/
│
├── app/
│   ├── core/          # Configuration & settings
│   ├── db/            # Database engine & session
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── repository/    # Database access layer
│   ├── services/      # Business logic
│   ├── routers/       # API routes
│   └── utils/         # Auth, email, helpers
│
├── main.py
├── .gitignore
├── .env.example
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/manjeetbargoti/fastapi-auth.git
cd fastapi-auth
```

---

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate     # Linux / Mac
venv\Scripts\activate        # Windows
```

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. PostgreSQL Setup

Create a PostgreSQL database:
```sql
CREATE DATABASE fastapi_auth;
```

---

### 5. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/fastapi_auth
JWT_SECRET_KEY=your_super_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
FRONTEND_URL=http://localhost:3000

MAIL_USERNAME=example@gmail.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=example@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_TLS=True
MAIL_SSL=False
```

---

### 6. Run the Application
```bash
uvicorn main:app --reload
```

API:
```
http://127.0.0.1:8000
```

Docs:
```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

1. Signup → verification email sent  
2. Verify email  
3. Login → JWT issued  

---

## 🧪 Core API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /auth/signup | Register user |
| POST | /auth/login | Login user |
| GET  | /auth/verify-email | Verify email |
| GET  | /protected | Protected route |

---

## 🔒 Security Practices

- Password hashing with bcrypt  
- Email verification enforced  
- JWT with expiration  
- Secrets via environment variables  
- PostgreSQL constraints  

---

## 🛣️ Roadmap

- Refresh tokens  
- RBAC  
- Alembic migrations  
- Async SQLAlchemy  
- Docker support  

---

## 📄 License

MIT License

---

## 👤 Author

**Manjeet Bargoti**  
GitHub: https://github.com/manjeetbargoti
