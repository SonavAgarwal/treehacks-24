from fastapi import APIRouter
from app.utils.github import *
from app.utils.analysis import *

router = APIRouter()


@router.get("/testing")
async def test():
    repos = [GitRepository('HIST5', 'https://github.com/sophiasharif/HIST5'),
             GitRepository('study-samurai', 'https://github.com/sophiasharif/study-samurai')]
    download_repos(repos)

    repos = await fetch_repos("sophiasharif")
    # files = fetch_files(repos, "sophiasharif")
    print(repos)



# repos = [GitRepository('HIST5', 'https://github.com/sophiasharif/HIST5'),
#          GitRepository('study-samurai', 'https://github.com/sophiasharif/study-samurai')]
# download_repos(repos)

# files = fetch_files(repos, "sophiasharif")
# print(files)


# user_repos = fetch_repos("sophiasharif")
# for repo in user_repos:
#     print("REPO ", repo.name)
#     print(repo.url)
#     print(repo.description)
#     print(repo.languages)
#     print(repo.commits)
#     print(repo.last_modified)