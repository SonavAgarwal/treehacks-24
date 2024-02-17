import shutil
import subprocess
import os
import openai
import requests
from app.models.git_models import *

together_key = os.getenv("TOGETHER_KEY")

# api function calls these in order
# 1 - query graphql --> all the repos and metadata (sophia)
# 1.5 - calculate relevance of repos (sonav)
# 2 - download relevant repos (sophia) (process into repo object)
# 2.5 - get relevant files (sonav) --> file objects that are relevant
# 3 - get relevant code (sophia) (git blame for relevant files)
# 3.5 - score the code based on the query (sonav)

# class GitRepository:
#     def __init__(self, name, url):
#         self.name = name
#         self.url = url
#         self.description = ""
#         self.languages = [] # TODO: sort this by frequency or something (just a list of strings for now)
#         self.files = []
#         self.commits = []
#         self.last_modified = None


# class GitFile:
#     def __init__(self, path, num_commits):
#         self.path = path  # includes the name
#         self.num_commits = num_commits
#         self.score = 0
#         self.relevant_code = []

#     def __repr__(self):
#         return f"File: {self.path} - {self.num_commits} commits"


# class GitCommit:
#     def __init__(self, sha, message, date):
#         self.sha = sha
#         self.message = message
#         self.date = date
#         self.files = []

#     def __repr__(self):
#         return f"Commit: {self.sha[:4]} - {self.message} - {self.date}"


def create_repository_objects(query_outputs, user_username):
    repositories = []
    for repo_data in query_outputs:
        try:
            repo = GitRepository(repo_data['name'], repo_data['url'])
            repo.description = repo_data['description'] if repo_data['description'] else None
            repo.languages = [lang['node']['name']
                              for lang in repo_data['languages']['edges']]
            repo.commits = []
            for commit in repo_data['defaultBranchRef']['target']['history']['edges']:
                if user_username not in commit['node']['author']['email']:
                    continue
                sha = commit['node']['oid']
                message = commit['node']['message']
                date = commit['node']['committedDate']
                repo.commits.append(GitCommit(sha, message, date))
            repo.last_modified = repo.commits[0].date
            repositories.append(repo)
        except Exception as e:
            print(f"Error creating repository {repo_data['name']} object: {e}")
    return repositories


def fetch_repos(user_username):
    url = 'https://api.github.com/graphql'
    # TODO: update the query so that only commits the user has made are fetched
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
                author {
                  email
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
        repos = create_repository_objects(repositories, user_username)
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
        clone_command = f"git clone {repo.url} {repo_path}"

        try:
            subprocess.run(clone_command, check=True, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Check the size of the cloned repo
            total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                             for dirpath, dirnames, filenames in os.walk(repo_path) for filename in filenames)
            total_size_mb = total_size / (1024 * 1024)  # Convert bytes to MB

            if total_size_mb > size_limit_mb:
                print(repo.name, "exceeds the size limit of", size_limit_mb,
                      "MB. Deleting the cloned repo...")
                shutil.rmtree(repo_path)
            else:
                print(f"Cloned {repo.name} successfully")

        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo.name}: {e}")

    my_var_1 = "hello"
    my_var_2 = 13924
    print(f"{my_var_1} exceeds the size limit of {my_var_2} MB. Deleting...")


def fetch_files(repos, username):
    clone_dir = "/usr/cloned_repos"
    files_contributed = []  # To store tuples of (file, num_occurrences)
    for repo in repos:
        user = repo.url.split('/')[-2]
        repo_path = os.path.join(clone_dir, user, repo.name)
        os.chdir(repo_path)  # Change working directory to the repo's path

        # Constructing the git log command
        git_command = f'git log --author="{username}" --pretty="" ' + \
            '--name-only | sort | uniq -c | sort -rn'

        # Execute the git command
        try:
            output = subprocess.check_output(
                git_command, shell=True, text=True)
            # Parsing the output
            for line in output.strip().split('\n'):
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    num_occurrences, file_name = int(parts[0]), parts[1]
                    files_contributed.append(
                        GitFile(file_name, num_occurrences))
        except subprocess.CalledProcessError as e:
            print(f"Error executing git command: {e}")

    return files_contributed


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
