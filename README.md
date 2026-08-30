# Lynktern AI Engine — Logbook Generator Module

Stateless FastAPI module inside the Lynktern AI Processing Engine. Converts a
student's raw internship activities into a formal, first-person SIWES logbook
paragraph.

This module does exactly one thing: **text in, text out.** It does not call OCR,
does not process PDFs/images, does not touch a database, and does not run
background/batch jobs. Persistence and orchestration are the Next.js app's job.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # fill in MISTRAL_API_KEY
```

## Run

```bash
uvicorn app.main:app --reload
```

## Endpoint

`POST /ai/logbook/generate`

Request:
```json
{
  "activities": ["built login page", "connected Supabase database", "fixed API bugs"],
  "skills": ["React", "Supabase"]
}
```

Response:
```json
{
  "formatted_entry": "I developed a functional login interface...",
  "summary": "authentication system and backend integration work completed"
}
```

`GET /health` - health check.

## How it connects

```
Next.js sends raw log
        |
POST /ai/logbook/generate
        |
Python formats it (Mistral)
        |
returns { formatted_entry, summary }
        |
Next.js saves it to Supabase
```

This module owns none of the Supabase schema or credentials - the caller (Next.js)
is responsible for persisting the result.
