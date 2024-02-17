from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.analysis import *
from app.utils.github import *
from app.models.analysis_models import *

router = APIRouter()


class AnalyzeAccountRequest(BaseModel):
    username: str
    queries: List[CodeAnalysisQuery]


@router.post("/analyze_account")
async def analyze_account(body: AnalyzeAccountRequest):
    username = body.username
    queries = body.queries

    repos = fetch_repos(username)
    repos = process_repos(repos)

    repo_and_scores = await find_best_repos(repos, queries)
    print(repo_and_scores)
    return repo_and_scores
