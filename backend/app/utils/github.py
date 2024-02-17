from dotenv import load_dotenv
import os
import openai
import requests
# from app.models.git_models import GitRepository

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

class GitRepository:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.description = ""
        self.languages = []
        self.files = []
        self.commits = []


class GitFile:
    def __init__(self, name, path, url):
        self.path = path  # includes the name
        self.score = 0
        self.relevant_code = []


class GitCommit:
    def __init__(self, sha, message, date):
        self.sha = sha
        self.message = message
        self.date = date
        self.files = []
    
    def __repr__(self):
        return f"Commit: {self.sha[:4]} - {self.message} - {self.date}"


def create_repository_objects(query_outputs):
    repositories = []
    for repo_data in query_outputs:
        repo = GitRepository(repo_data['name'], repo_data['url'])
        repo.description = repo_data['description'] if repo_data['description'] else ""
        repo.languages = [lang['node']['name'] for lang in repo_data['languages']['edges']]
        repo.commits = [GitCommit(commit['node']['oid'], commit['node']['message'], commit['node']['committedDate']) for commit in repo_data['defaultBranchRef']['target']['history']['edges']]
        repositories.append(repo)
    return repositories


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
                committedDate
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
        repos = create_repository_objects(repositories)
        return repos
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
for repo in user_repos:
    print("REPO ", repo.name)
    print(repo.url)
    print(repo.description)
    print(repo.languages)
    print(repo.commits)




# def get_github_user_id(username):
#     """Fetch GitHub user ID based on username."""
#     url = f"https://api.github.com/users/{username}"
#     headers = {'Accept': 'application/vnd.github.v3+json'}
    
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raises an HTTPError if the status is 4XX or 5XX
#         user_data = response.json()
#         return user_data.get('id')
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching user data: {e}")
#         return None

# username = 'sophiasharif'  # Replace 'octocat' with the actual GitHub username
# user_id = get_github_user_id(username)
# print(f"User ID for {username}: {user_id}")

