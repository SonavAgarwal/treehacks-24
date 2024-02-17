from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.analysis import find_best_filenames

router = APIRouter()


class AnalyzeAccountRequest(BaseModel):
    files: list[str]
    query: str


@router.post("/analyze_account")
async def analyze_account(body: AnalyzeAccountRequest):
    print("ANALYZE ACCOUNT CALLED")
    print(body)
    files = body.files
    query = body.query
    response = find_best_filenames(filenames=files, query=query)
    return response
