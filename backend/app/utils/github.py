import re
import shutil
import subprocess
import os
import aiohttp
from app.models.git_models import *
from datetime import datetime

together_key = os.getenv("TOGETHER_KEY")

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
                date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
                repo.commits.append(GitCommit(sha, message, date_obj))
            repo.last_modified = repo.commits[0].date if repo.commits else None
            repositories.append(repo)
        except Exception as e:
            print(f"Error creating repository {repo_data['name']} object: {e}")
    return repositories


async def fetch_repos(user_username):
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

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json={'query': query}) as response:
            if response.status == 200:
                data = await response.json()
                repositories = data['data']['user']['repositories']['nodes']
                repos = create_repository_objects(repositories, user_username)
                return repos
            else:
                print('Failed to fetch repositories:', await response.text())
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


def process_grep_output(output: str):
    pattern = re.compile(r'\S+ \(\S+ \S+ \S+ \S+ (\d+)\) (.*)')
    lines_written = []

    for line in output.strip().split('\n'):
        match = pattern.match(line)
        if match:
            line_number, code_line = match.groups()
            lines_written.append((int(line_number), code_line))

    code_chunks = []
    for i in range(len(lines_written)):
        if i == 0 or lines_written[i][0] != lines_written[i-1][0] + 1:
            code_chunks.append(lines_written[i][1])
        else:
            code_chunks[-1] += '\n' + lines_written[i][1]
    return code_chunks

def fetch_files(repos, username):
    clone_dir = "/usr/cloned_repos"
    res = []
    
    # get files changed & number of commits they occur in
    for repo in repos:
        user = repo.url.split('/')[-2]
        repo_path = os.path.join(clone_dir, user, repo.name)
        os.chdir(repo_path)  # Change working directory to the repo's path

        # Constructing the git log command
        git_command = f'git log --author="{username}" --pretty="" ' + \
            '--name-only | sort | uniq -c | sort -rn'
        
        # get list of files contributed to
        files_contributed = []  # To store tuples of (file, num_occurrences)
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
        
        final_files = []
        for file in files_contributed:
          try:
            blame_command = f'git blame {file.path} | grep "sophiasharif"'
            output = subprocess.check_output(
              blame_command, shell=True, text=True)
            code_chuks = process_grep_output(output)
            file.relevant_code = code_chuks
            final_files.append(file)
          except subprocess.CalledProcessError as e:
              print(f"File not found: {e}")

    return res

