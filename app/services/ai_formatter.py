import json
from functools import lru_cache
from typing import List, Tuple

from mistralai.client import Mistral
from mistralai.client.errors import MistralError

from app.config import get_settings

SYSTEM_PROMPT = """You convert a student's raw internship activities into a formal \
SIWES (Nigerian Students Industrial Work Experience Scheme) logbook entry.

Style rules:
- Write in FIRST PERSON, past tense only, formal academic tone.
- Expand the raw tasks into one clean flowing narrative paragraph - no bullet \
points, no headings.
- Do not exaggerate the work done, and do not invent tools or technologies not \
present in the input.
- Do not mention the day of the week or a week number.
- End with a clear outcome or skill gained.

Respond with ONLY a JSON object with exactly two keys:
- "formatted_entry": the full formal paragraph described above.
- "summary": a short (under 15 words) lowercase phrase summarizing the work, e.g. \
"authentication system and backend integration work completed"."""


@lru_cache
def _get_client() -> Mistral:
    settings = get_settings()
    return Mistral(api_key=settings.mistral_api_key)


def generate_logbook_entry(activities: List[str], skills: List[str]) -> Tuple[str, str]:
    settings = get_settings()
    client = _get_client()

    activities_block = "\n".join(f"- {a}" for a in activities)
    skills_block = f"\n\nSkills/tools: {', '.join(skills)}" if skills else ""

    try:
        response = client.chat.complete(
            model=settings.mistral_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Activities:\n{activities_block}{skills_block}",
                },
            ],
        )
    except MistralError as exc:
        raise RuntimeError(f"AI formatting failed: {exc}") from exc

    choice = response.choices[0] if response.choices else None
    content = choice.message.content if choice and choice.message else None
    if isinstance(content, list):
        content = "".join(getattr(chunk, "text", "") for chunk in content)

    if not content or not content.strip():
        raise RuntimeError("AI formatting returned an empty response")

    try:
        parsed = json.loads(content)
        formatted_entry = str(parsed["formatted_entry"]).strip()
        summary = str(parsed["summary"]).strip()
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise RuntimeError(f"AI returned an unexpected response shape: {content!r}") from exc

    if not formatted_entry or not summary:
        raise RuntimeError("AI formatting returned an empty field")

    return formatted_entry, summary
