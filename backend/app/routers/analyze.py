from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.analysis import *
from app.utils.github import *
from app.models.analysis_models import *
from asyncio import gather

router = APIRouter()


class AnalyzeAccountRequest(BaseModel):
    username: str
    queries: List[str] = []
    criteria: List[str] = []


@router.post("/analyze_account")
async def analyze_account(body: AnalyzeAccountRequest):
    username = body.username
    queries = body.queries
    criteria = body.criteria

    print("Analyzing account", username, flush=True)

    # Schedule both tasks to run in parallel
    queries_task = construct_queries(queries)
    repos_task = fetch_repos(username)
    completed_tasks = await gather(queries_task, repos_task)

    # Unpack the results
    queries, repos = completed_tasks

    await calculate_relevance(repos, queries)

    for repo in repos:
        print(json.dumps(repo.__dict__), flush=True)

    return

    # repo_and_scores = await calculate_relevance(repos, queries)
    # for rs in repo_and_scores:
    #     repo, scores = rs
    #     print(repo.name, repo.description, flush=True)
    #     for key in scores:
    #         query_num = -1
    #         try:
    #             query_num = int(key.split("_")[1])
    #             print("\t", queries[query_num].query,
    #                   "\t\t\t\t", scores[key], flush=True)
    #         except:
    #             print("Error parsing query number", key, flush=True)
    #         pass
    #     pass

    # print(repo_and_scores)
    # download relevant repos

    # for each query, determine the 3 best repos for that query
    # download the relevant files for each repo

    # TODO: PICK MORE RELEVANT REPOS BASED ON HOW MUCH YOU'VE CONTRIBUTED, ETC
    # TODO: CUT REPOS WITH VERY LITTLE CODE
    # TODO: CUT REPOS WITH NO RECENT COMMITS
    # TODO: DO THESE EARLIER
    # TODO: LOOK FOR PINNED REPOS

    relevant_repos = set()
    for i, query in enumerate(queries):
        query_str = "query_" + str(i)
        sorted_repos = sorted(
            repo_and_scores, key=lambda x: x[1][query_str], reverse=True)
        for repo, score in sorted_repos[:3]:
            relevant_repos.add(repo)
        print(query.query, ":", ", ".join([
              repo.name for repo, scores in sorted_repos[:3]]), flush=True)

    # download_repos(repo_and_scores)

    return repo_and_scores
