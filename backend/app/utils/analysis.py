import json
from dotenv import load_dotenv
import os
import openai
# from config import config
import asyncio

config = {
    "MODEL_STRING": "mistralai/Mistral-7B-Instruct-v0.1"
}

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

async def calculate_relevance(repos, queries):
    tasks = [evaluate_repo_relevance(
        repo, queries, client) for repo in repos]
    return_repos = await asyncio.gather(*tasks)
    return return_repos


def find_relevant_files(repos, query):
    # NOTE: doesn't filter based on whether the user has written to the file or not
    tasks = [evaluate_files_relevance(
        repo, query, client) for repo in repos]
    return_files = asyncio.gather(*tasks)
    return return_files


def score_code(files, queries):
    return None  # return files


# ===========================
# helper functions
# ===========================

def repo_to_string(repo):
    # shortened_description = await shorten_description(repo.description)
    string = f"Repo name:{repo.name}\n"
    if (repo.description):
        string += f"Description:{repo.description}\n"
    if (len(repo.languages) > 0):
        string += f"Languages:{', '.join(repo.languages)}\n"

    most_useful_commit_messages = []
    for commit in repo.commits:
        if len(most_useful_commit_messages) > 30:
            break
        # make sure it doesn't start with "Merge"
        # make sure its longer than 10 characters
        lower_message = commit.message.lower()
        starts_with_merge = lower_message.startswith("merge")
        starts_with_update = lower_message.startswith("update")
        if not starts_with_merge and not starts_with_update and len(commit.message) > 10:
            most_useful_commit_messages.append(commit.message)
    if len(most_useful_commit_messages) > 0:
        commits = "\n".join(most_useful_commit_messages)
        string += f"Commits:\n{commits}\n"
    return string


async def process_repos(repos):
    print("Processing repos", flush=True)

    tasks = [shorten_description(repo.description) for repo in repos]
    descriptions = await asyncio.gather(*tasks)

    # Updating repo descriptions with their shortened versions
    for repo, description in zip(repos, descriptions):
        repo.description = description

    return repos

    # async def process_repo(repo):
    #     repo.description = await shorten_description(repo.description)
    #     return repo

    # tasks = [process_repo(repo) for repo in repos]
    # return_repos = await asyncio.gather(*tasks)
    # return return_repos


async def shorten_description(description):
    print("Shortening description of repo" +
          description[:10] + "...", flush=True)
    instructions = f"""
        You are given a README of a Github repository and asked to shorten it to 200 characters or less.
        Return the shortened description as a string.
    """
    response = client.chat.completions.create(
        model=config["MODEL_STRING"],
        messages=[
            {
                "role": "system",
                "content": instructions
            }, {
                "role": "user",
                "content": description[:200]
            }
        ],
    )

    first_choice = response.choices[0]
    completion = first_choice.message.content
    return completion


async def evaluate_repo_relevance(repo, queries, client):
    instructions = """
        You are given a Github repository and asked to calculate the relevance of the repository to the given queries.
        For each query the relevance in a JSON object as follows: "query_N": relevance. 0 <= relevance <= 10
        """

    input_string = ""

    repo_string = repo_to_string(repo)
    input_string += repo_string + "\n"

    for i, query in enumerate(queries):
        input_string += f"query_{i}: {query.query}\n"

    response = client.chat.completions.create(
        model=config["MODEL_STRING"],
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": instructions
            }, {
                "role": "user",
                "content": input_string
            }
        ],
    )
    completion = json.loads(response.choices[0].message.content)
    print(repo_string, "\n --> \n", completion, "\n\n\n", flush=True)
    return (repo, completion)


async def evaluate_files_relevance(repo, query, client):
    prompt = f"""
        You are given a Github repository and the files in it. You are asked to calculate the relevance of the files to the given queries.
        For each query the relevance in a JSON object as follows: "full_file_path": relevance. 0 <= relevance <= 10
    """
    input_string = ""

    repo_string = repo_to_string(repo)
    input_string += repo_string

    input_string += "query: " + query + "\n"

    files = [file.path for file in repo.files]
    input_string += f"file paths:\n"
    for file in files:
        input_string += f"{file}\n"

    response = client.chat.completions.create(
        model=config["MODEL_STRING"],
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": prompt
            }, {
                "role": "user",
                "content": input_string
            }
        ],
    )

    completion = json.loads(response.choices[0].message.content)

    return completion


# # repos will be ()

# # ===========================
# # find_best_repos(repos, query)
# # repos[]: list of repos

# # ===========================


# def find_best_repos(repos, query):
#     return None

# # ===========================
# # find_best_filenames(file_names, query)
# # ===========================


# def find_best_filenames(filenames, query):
#     prompt = f"""
#         You are looking for files that are most relevant to the given query, and returning a score for each file in JSON format.
#         For each file, score it from 1 to 10 based on how likely it is to be relevant to the query.
#         The higher the score, the more relevant the file is.
#         If you are not sure, set score to -1.
#         For example:
#         query: code that uses axios
#         files: main.js, api.js, index.js, package.json, README.md
#         would be converted to:
#         {{
#             scores: {{
#                 "main.js": 7,
#                 "api.js": 9,
#                 "index.js": 4,
#                 "package.json": 0,
#                 "README.md": 0,
#             }}
#         }}
#     """

#     print(prompt)

#     response = client.chat.completions.create(
#         model=config["MODEL_STRING"],
#         messages=[
#             {
#                 "role": "system",
#                 "content": prompt
#             }, {
#                 "role": "user",
#                 "content": f"query: {query}\nfiles: {', '.join(filenames)}"
#             }
#         ],
#         response_format={
#             "type": "json_object",
#         }
#     )

#     return response
