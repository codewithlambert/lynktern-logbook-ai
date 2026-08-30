from typing import List

from pydantic import BaseModel, Field


class LogbookGenerateRequest(BaseModel):
    activities: List[str] = Field(min_length=1)
    skills: List[str] = Field(default_factory=list)


class LogbookGenerateResponse(BaseModel):
    formatted_entry: str
    summary: str
