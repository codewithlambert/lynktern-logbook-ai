from fastapi import FastAPI

from app.routes import logbook

app = FastAPI(
    title="Lynktern AI Engine - Logbook Generator",
    description="Stateless text-in/text-out module: raw student activities -> formal SIWES logbook entry.",
    version="0.1.0",
)

app.include_router(logbook.router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
