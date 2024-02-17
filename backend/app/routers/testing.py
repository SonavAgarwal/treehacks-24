from fastapi import APIRouter
from app.utils.github import *
from app.utils.analysis import *

router = APIRouter()


@router.get("/testing")
async def test():
    repos = [GitRepository('HIST5', 'https://github.com/sophiasharif/HIST5'),
             GitRepository('study-samurai', 'https://github.com/sophiasharif/study-samurai')]
    download_repos(repos)

    files = fetch_files(repos, "sophiasharif")
    print(files)
