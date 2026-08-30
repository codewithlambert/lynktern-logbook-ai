# Lynktern AI Engine — Logbook Generator Module

A stateless FastAPI microservice within the Lynktern AI Processing Engine.

This module transforms a student’s raw internship activities into a **formal, first-person SIWES logbook entry** using AI.

---

 Purpose

The Logbook Generator is intentionally minimal and focused:

> **Text in → Structured SIWES entry out**

It does **one job only**:

* Converts raw activity inputs into a polished academic logbook paragraph

---

#What this module does NOT do

To maintain clean architecture boundaries, this service:

* ❌ Does not perform OCR
* ❌ Does not process PDFs or images
* ❌ Does not interact with any database
* ❌ Does not handle authentication or user sessions
* ❌ Does not run background or batch jobs

All persistence and orchestration are handled by the **Next.js backend**.

---

## ⚙️ Setup

```bash
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env
# Fill in:
# MISTRAL_API_KEY
# INTERNAL_API_SECRET
```

---

## ▶️ Run the service

```bash
uvicorn app.main:app --reload
```

---

## 🔌 API Endpoints

### `POST /ai/logbook/generate`

Generates a formatted SIWES logbook entry.

#### 🔐 Security

Requires header:

```
X-Internal-Secret: <INTERNAL_API_SECRET>
```

* Missing or invalid → `401 Unauthorized`
* This is **not user authentication**
* It is a shared internal secret between this service and the Next.js backend
* Prevents unauthorized usage of your AI quota

---
 Request

```json
{
  "activities": [
    "built login page",
    "connected Supabase database",
    "fixed API bugs"
  ],
  "skills": [
    "React",
    "Supabase"
  ]
}
```

---

 Response

```json
{
  "formatted_entry": "I developed a functional login interface...",
  "summary": "authentication system and backend integration work completed"
}
```

---

 Health Check

```
GET /health
```

Returns service status.

---

 System Flow

```
Next.js (Lynktern)
        ↓
POST /ai/logbook/generate
        ↓
AI Engine (Mistral processes input)
        ↓
Returns formatted_entry + summary
        ↓
Next.js stores result in Supabase
```

---

 Design Philosophy

This module is built as a **pure AI transformation service**:

* Stateless
* Fast (<10s response time)
* Single responsibility
* Easily replaceable or scalable

It **does not own data** — it only transforms it.

---

 Role in Lynktern Architecture

| Layer                   | Responsibility                       |
| ----------------------- | ------------------------------------ |
| Next.js                 | UI, auth, orchestration, persistence |
| AI Engine (this module) | Text → SIWES logbook transformation  |
| Supabase                | Data storage                         |

---

 Summary

This module is a lightweight, production-ready AI microservice designed to:

* Standardize SIWES logbook entries
* Offload AI processing from the frontend
* Maintain clean separation of concerns in the Lynktern system

---

## 📌 Note

All database operations, schema management, and user-level logic are handled externally by the Next.js application.

This service remains strictly **stateless and compute-focused**.
