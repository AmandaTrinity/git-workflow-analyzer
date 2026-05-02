import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GithubCollector:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is not set")
        self.g = Github(token)

    def test_connection(self, repo_name):
        try:
            repo = self.g.get_repo(repo_name)
            print(f"Successfully connected to {repo_name}")
        except Exception as e:
            print(f"Error connecting to {repo_name}: {e}")
            return False
        return True
if __name__ == "__main__":
    collector = GithubCollector()
    repo_to_test = os.getenv("GITHUB_REPO")
    if not repo_to_test:
        raise ValueError("GITHUB_REPO environment variable is not set")
    collector.test_connection(repo_to_test)