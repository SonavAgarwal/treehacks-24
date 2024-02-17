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
