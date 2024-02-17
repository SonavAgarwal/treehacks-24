from dotenv import load_dotenv
import os
import openai

load_dotenv()
together_key = os.getenv("TOGETHER_KEY")

client = openai.OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=together_key)

# api function calls these in order
# 1 - query graphql --> all the repos and metadata (sophia)
# 1.5 - calculate relevance of repos (sonav)
# 2 - download relevant repos (sophia) (process into repo object)
# 2.5 - get relevant files (sonav) --> file objects that are relevant
# 3 - get relevant code (sophia) (git blame for relevant files)
# 3.5 - score the code based on the query (sonav)


def fetch_repos(user_username):
    return None  # return repos


def download_repos(repos):
    return None  # return repos


def fetch_files(repos):
    # using git blame to get relevant code
    return None  # return files
