

CODE_ANALYSIS_TYPES = ["structure", "complexity",
                       "performance", "implementation", "data", "problem_solving"]

# structure: how well the code is organized
# complexity: how complex the code is
# performance: how well the code performs (speed and memory)
# implementation: how well the code implements the requirements
# data: how well the code handles and manipulates data
# problem_solving: how well the code solves problems


class CodeAnalysisQuery:
    def __init__(self, query_id, original_query):
        self.query_id = query_id
        self.original_query = original_query

        self.query = ""
        self.query_type = ""

        # self.repos = []
        # self.files = []
        # self.best_repos = []
        # self.best_files = []

# ===========================
# tools are things like libraries, frameworks, and languages
# ===========================


class ToolAnalysisQuery:
    def __init__(self, query):
        self.query = query
        self.query_type = ""
        self.tools = []
        self.best_tools = []


class Tool:
    def __init__(self, name, description, url, score):
        self.name = name
        self.score = score
