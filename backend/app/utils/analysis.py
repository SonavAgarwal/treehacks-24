from dotenv import load_dotenv
import os
import openai
import config
import asyncio

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
        repo, queries, client, config) for repo in repos]
    return_repos = await asyncio.gather(*tasks)
    return return_repos


def find_relevant_files(repos, query):
    # NOTE: doesn't filter based on whether the user has written to the file or not
    tasks = [evaluate_files_relevance(
        repo, query, client, config) for repo in repos]
    return_files = asyncio.gather(*tasks)
    return return_files


def score_code(files, queries):
    return None  # return files


# ===========================
# helper functions
# ===========================

async def repo_to_string(repo):
    # shortened_description = await shorten_description(repo.description)
    string = f"Repo name:{repo.name}\n"
    string += f"Description:{repo.description}\n"
    string += f"Languages:{', '.join(repo.languages)}\n"
    commits = "\n".join([f"{commit.message}" for commit in repo.commits])
    string += f"Commits:\n{commits}\n"
    return string


async def process_repos(repos):
    async def process_repo(repo):
        repo.description = await shorten_description(repo.description)
        return repo

    tasks = [process_repo(repo) for repo in repos]
    return_repos = await asyncio.gather(*tasks)
    return return_repos


async def shorten_description(description):
    instructions = f"""
        You are given a README of a Github repository and asked to shorten it to 200 characters or less.
        Return the shortened description in a JSON object with the key "desc".
    """
    response = await client.chat.completions.create(
        model=config.MODEL_STRING,
        messages=[
            {
                "role": "system",
                "content": instructions
            }, {
                "role": "user",
                "content": description
            }
        ],
        response_format={
            "type": "json_object",
        }
    )
    completion = response.choices[0].message['content']
    return completion.get('desc', "")


async def evaluate_repo_relevance(repo, queries, client, config):
    instructions = """
        You are given a Github repository and asked to calculate the relevance of the repository to the given queries.
        For each query the relevance in a JSON object as follows: "query_N": relevance. 0 <= relevance <= 10
        """

    input_string = ""

    repo_string = await repo_to_string(repo)
    input_string += repo_string

    for i, query in enumerate(queries):
        input_string += f"query_{i}: {query.query}\n"

    response = await client.chat.completions.create(
        model=config.MODEL_STRING,
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
    completion = response.choices[0].message['content']
    return (repo, completion)


async def evaluate_files_relevance(repo, query, client, config):
    prompt = f"""
        You are given a Github repository and the files in it. You are asked to calculate the relevance of the files to the given queries.
        For each query the relevance in a JSON object as follows: "full_file_path": relevance. 0 <= relevance <= 10
    """
    input_string = ""

    repo_string = await repo_to_string(repo)
    input_string += repo_string

    input_string += "query: " + query + "\n"

    files = [file.path for file in repo.files]
    input_string += f"file paths:\n"
    for file in files:
        input_string += f"{file}\n"

    response = client.chat.completions.create(
        model=config.MODEL_STRING,
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

    completion = response.choices[0].message['content']
    return completion


# repos will be ()

# ===========================
# find_best_repos(repos, query)
# repos[]: list of repos

# ===========================


def find_best_repos(repos, query):
    return None

# ===========================
# find_best_filenames(file_names, query)
# ===========================


def find_best_filenames(filenames, query):
    prompt = f"""
        You are looking for files that are most relevant to the given query, and returning a score for each file in JSON format.
        For each file, score it from 1 to 10 based on how likely it is to be relevant to the query.
        The higher the score, the more relevant the file is.
        If you are not sure, set score to -1.
        For example:
        query: code that uses axios
        files: main.js, api.js, index.js, package.json, README.md
        would be converted to:
        {{
            scores: {{
                "main.js": 7,
                "api.js": 9,
                "index.js": 4,
                "package.json": 0,
                "README.md": 0,
            }}
        }}
    """

    print(prompt)

    response = client.chat.completions.create(
        model=config.MODEL_STRING,
        messages=[
            {
                "role": "system",
                "content": prompt
            }, {
                "role": "user",
                "content": f"query: {query}\nfiles: {', '.join(filenames)}"
            }
        ],
        response_format={
            "type": "json_object",
        }
    )

    return response
