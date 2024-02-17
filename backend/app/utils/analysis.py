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

def calculate_relevance(repos, queries):
    return None  # return repos


def find_relevant_files(repos, queries):
    return None  # return files


def score_code(files, queries):
    return None  # return files


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
        model="mistralai/Mistral-7B-Instruct-v0.1",
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
