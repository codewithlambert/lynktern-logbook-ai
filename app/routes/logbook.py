from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import LogbookGenerateRequest, LogbookGenerateResponse
from app.security import require_internal_secret
from app.services.ai_formatter import generate_logbook_entry

router = APIRouter(prefix="/ai/logbook", tags=["logbook"])


@router.post(
    "/generate",
    response_model=LogbookGenerateResponse,
    dependencies=[Depends(require_internal_secret)],
)
def generate(payload: LogbookGenerateRequest) -> LogbookGenerateResponse:
    """Stateless: raw activities/skills in, formatted SIWES entry out. No persistence."""
    try:
        formatted_entry, summary = generate_logbook_entry(
            activities=payload.activities, skills=payload.skills
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return LogbookGenerateResponse(formatted_entry=formatted_entry, summary=summary)
