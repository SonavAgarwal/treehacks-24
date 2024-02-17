from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.analysis import *
from app.utils.github import *
from app.models.analysis_models import *

router = APIRouter()


class AnalyzeAccountRequest(BaseModel):
    username: str
    queries: List[str]


@router.post("/analyze_account")
async def analyze_account(body: AnalyzeAccountRequest):
    print("Analyzing account")
    print(body)
    # return None
    username = body.username
    queries = body.queries
    queries = [CodeAnalysisQuery(query=query) for query in queries]

    repos = fetch_repos(username)
    print("REPOS: ", repos, flush=True)
    # repos = await process_repos(repos)
    # for repo in repos:
    #     print(repo.name, repo.description, flush=True)

    repo_and_scores = await calculate_relevance(repos, queries)
    for rs in repo_and_scores:
        repo, scores = rs
        print(repo.name, repo.description, flush=True)
        for key in scores:
            query_num = -1
            try:
                query_num = int(key.split("_")[1])
                print("\t", scores[key], " --> ",
                      queries[query_num].query, flush=True)
            except:
                pass
    # print(repo_and_scores)
    return repo_and_scores
