# Behavix Backend

AI-powered user behavior analytics API built with FastAPI, PostgreSQL, and Groq LLaMA 3.3.

## Features
- Company registration with auto-generated API keys
- Event ingestion (page visits, button clicks, signups, feature usage)
- Analytics endpoints (overview, trends, top pages, buttons, features)
- Suspicious IP detection
- AI-generated insights via Groq LLaMA 3.3 70B
- JWT authentication
- Rate limiting, input validation, Alembic migrations
- Docker support

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy + Alembic
- **AI:** Groq LLaMA 3.3 70B
- **Auth:** JWT
- **Deployment:** Render

## Setup

1. Clone the repo:
```bash
git clone https://github.com/Ailesh69/behavix-backend.git
cd behavix-backend
```

2. Create virtual environment:
```bash
python -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/behavix
SECRET_KEY=your-secret-key
ALGORITHM=HS256
GROQ_API_KEY=your-groq-api-key
```

5. Run migrations:
```bash
alembic upgrade head
```

6. Start server:
```bash
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

## Docker
```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /auth/register` — Register company, get API key
- `POST /auth/login` — Login, get JWT token

### Events
- `POST /events` — Ingest event (X-API-Key header)
- `GET /events` — Get events (JWT)

### Analytics
- `GET /analytics/overview` — Total events, signups, active users
- `GET /analytics/trends` — 30-day event trends
- `GET /analytics/pages` — Top visited pages
- `GET /analytics/buttons` — Top clicked buttons
- `GET /analytics/features` — Feature usage
- `GET /analytics/suspicious-ips` — Flagged IPs

### AI Insights
- `GET /insights/` — AI-generated insights

### Company
- `GET /company/me` — Company profile + API key
- `POST /company/regenerate-key` — Regenerate API key

## License
MIT