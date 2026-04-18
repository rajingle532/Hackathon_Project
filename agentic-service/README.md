# 🌾 Krishi Sakhi — Agentic Service

Multi-agent AI service for the Krishi Sakhi agricultural platform.

## Quick Start

```bash
# 1. Navigate to this folder
cd agentic-service

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env → set GOOGLE_API_KEY

# 5. Start the service
python main.py
```

The service starts on **http://localhost:8080**.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/ready` | Readiness probe |
| GET | `/docs` | Swagger UI |
| POST | `/agent/chat` | Agent chat (Module 2+) |

## Prerequisites

- Python 3.10+
- Express backend running on `:5000`
- ML API running on `:8001` (optional for Module 1)
- Disease API running on `:5050` (optional for Module 1)

## Testing

```bash
pytest tests/test_health.py -v
```

## Architecture

```
Frontend (React :5173)
  → Backend (Express :5000)
    → Agentic Service (FastAPI :8080)
      → Gemini LLM
      → LangGraph (Module 2)
      → CrewAI Agents (Module 3+)
      → ChromaDB RAG (Module 6)
      → Hindsight Memory (Module 10)
```
