from dotenv import load_dotenv
import os
import openai
import requests

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


import requests
import json

def fetch_repos(user_username):
    url = 'https://api.github.com/graphql'
    access_token = os.getenv("GITHUB_TOKEN")
    query = """
    {
      user(login: "%s") {
        repositories(first: 100) {
          nodes {
            name
            url
            description
            languages(first: 10) {
              edges {
                node {
                  name
                }
                size
              }
            }
            defaultBranchRef {
            name
            target {
                ... on Commit {
          history(first: 100) { 
            pageInfo {
              endCursor
              hasNextPage
            }
            edges {
              node {
                oid
                message
              }
            }
          }
        }
            }
            }
          }
        }
      }
    }
    """ % (user_username)

    # Request headers
    headers = {
        'Authorization': f'bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Make the GraphQL request
    response = requests.post(url, headers=headers, json={'query': query})

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        repositories = data['data']['user']['repositories']['nodes']
        return repositories
    else:
        print('Failed to fetch repositories:', response.text)
        return None


def download_repos(repos):
    return None  # return repos


def fetch_files(repos):
    # using git blame to get relevant code
    return None  # return files

fetch_repos("sophiasharif")
user_repos = fetch_repos("sophiasharif")
if user_repos:
    for repo in user_repos:
        print(repo)

def get_github_user_id(username):
    """Fetch GitHub user ID based on username."""
    url = f"https://api.github.com/users/{username}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the status is 4XX or 5XX
        user_data = response.json()
        return user_data.get('id')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None

# username = 'sophiasharif'  # Replace 'octocat' with the actual GitHub username
# user_id = get_github_user_id(username)
# print(f"User ID for {username}: {user_id}")

