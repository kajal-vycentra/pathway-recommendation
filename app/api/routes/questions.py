import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Request

from app.api.dependencies import verify_api_key
from app.schemas import EntryType
from app.core.rate_limit import rate_limit_default

router = APIRouter(tags=["Questions"])

# Base directory for data files
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


@router.get("/questions/{entry_type}")
@rate_limit_default
async def get_questions(
    request: Request,
    entry_type: EntryType,
    api_key: str = Depends(verify_api_key)
):
    """
    Get questionnaire questions based on entry type.

    Requires X-API-Key header.

    Args:
        entry_type: Either 'yes_i_know' or 'no_im_new'

    Returns:
        List of questions for the specified entry type
    """
    try:
        questions_path = BASE_DIR / "data" / "questions.json"
        with open(questions_path, "r", encoding="utf-8") as f:
            questions_data = json.load(f)

        flow_key = entry_type.value
        if flow_key not in questions_data["flows"]:
            raise HTTPException(status_code=404, detail=f"Flow '{flow_key}' not found")

        return {
            "entry_type": entry_type,
            "initial_question": questions_data["initial_question"],
            "questions": questions_data["flows"][flow_key]
        }
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Questions configuration not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid questions configuration")
