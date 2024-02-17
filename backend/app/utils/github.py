import shutil
import subprocess
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
        self.languages = [] # TODO: sort this by frequency or something (just a list of strings for now)
        self.files = []
        self.commits = []
        self.last_modified = None


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
        try:
          repo = GitRepository(repo_data['name'], repo_data['url'])
          repo.description = repo_data['description'] if repo_data['description'] else None
          repo.languages = [lang['node']['name'] for lang in repo_data['languages']['edges']]
          repo.commits = [GitCommit(commit['node']['oid'], commit['node']['message'], commit['node']['committedDate']) for commit in repo_data['defaultBranchRef']['target']['history']['edges']]
          repo.last_modified = repo.commits[0].date
          repositories.append(repo)
        except Exception as e:
          print(f"Error creating repository {repo_data['name']} object: {e}")
    return repositories


def fetch_repos(user_username):
    url = 'https://api.github.com/graphql'
    access_token = os.getenv("GITHUB_TOKEN") # TODO: update the query so that only commits the user has made are fetched
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


def download_repos(repos: list[GitRepository], size_limit_mb: int = 100):
    clone_dir = "/usr/cloned_repos"
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    
    for repo in repos:
        user = repo.url.split('/')[-2]
        repo_path = os.path.join(clone_dir, user, repo.name)
        print(repo_path)
        
        # Delete the repo directory if it already exists
        if os.path.exists(repo_path):
            print(f"{repo.name} already exists. Deleting existing directory.")
            shutil.rmtree(repo_path)
        
        print(f"Downloading {repo.name}")
        clone_command = f"git clone --depth 1 {repo.url} {repo_path}"
        
        try:
            subprocess.run(clone_command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Check the size of the cloned repo
            total_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(repo_path) for filename in filenames)
            total_size_mb = total_size / (1024 * 1024)  # Convert bytes to MB
            
            if total_size_mb > size_limit_mb:
                print(f"{repo.name} exceeds the size limit of {size_limit_mb}MB. Deleting...")
                shutil.rmtree(repo_path)
            else:
                print(f"Successfully cloned {repo.name}, size: {total_size_mb:.2f}MB")
                
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo.name}: {e}")



def fetch_files(repos):
    # using git blame to get relevant code
    return None  # return files

repos = [GitRepository('HIST5', 'https://github.com/sophiasharif/HIST5'), GitRepository('study-samurai', 'https://github.com/sophiasharif/study-samurai')]
download_repos(repos)


# user_repos = fetch_repos("SonavAgarwal")
# for repo in user_repos:
#     print("REPO ", repo.name)
#     print(repo.url)
#     print(repo.description)
#     print(repo.languages)
#     print(repo.commits)
#     print(repo.last_modified)




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

