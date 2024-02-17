from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.analysis import *
from app.utils.github import *
from app.models.analysis_models import *
from asyncio import gather
from operator import attrgetter


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
    queries: dict[str, CodeAnalysisQuery] = completed_tasks[0]
    repos_list: list[GitRepository] = completed_tasks[1]
    for i, repo in enumerate(repos_list):
        repo.repo_id = f"repo_{i}"
    repos: dict[str, GitRepository] = {
        repo.repo_id: repo for repo in repos_list}

    print("Fetched repos and queries", flush=True)

    await calculate_relevance(repos, queries)

    print("Calculated relevance", flush=True)

    # for repo in repos_list:
    #     print("===========", flush=True)
    #     print(repo.name, repo.description, flush=True)
    #     print(repo.query_relevances, flush=True)

    # download relevant repos

    # for each query, determine the 3 best repos for that query
    # download the relevant files for each repo

    # TODO: PICK MORE RELEVANT REPOS BASED ON HOW MUCH YOU'VE CONTRIBUTED, ETC
    # TODO: CUT REPOS WITH VERY LITTLE CODE
    # TODO: CUT REPOS WITH NO RECENT COMMITS
    # TODO: DO THESE EARLIER
    # TODO: LOOK FOR PINNED REPOS

    MAX_REPOS_PER_QUERY = 5
    MIN_RELEVANCE = 7

    repos_to_download = set()

    for query_id, query in queries.items():
        print("===========", flush=True)
        print(query_id, query.query, flush=True)

        sorted_repos = repos_list

        # remove repos that haven't been updated in the last 3 years
        sorted_repos = [repo for repo in sorted_repos if repo.last_modified >
                        datetime.now() - timedelta(days=365 * 3)]
        sorted_repos = [
            repo for repo in sorted_repos if repo.query_relevances[query_id] > MIN_RELEVANCE]

        sorted_repos = sorted(
            sorted_repos, key=lambda r: r.query_relevances[query_id], reverse=True)

        sorted_repos = sorted_repos[:MAX_REPOS_PER_QUERY]

        for repo in sorted_repos:
            print(repo.name, repo.query_relevances[query_id], flush=True)

        repos_to_download.update(sorted_repos)

    return

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
