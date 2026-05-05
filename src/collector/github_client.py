import os
from github import Github
from github import Auth

from dotenv import load_dotenv

load_dotenv()

class GithubCollector:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is not set")
        # Cliente conectado ao github
        auth = Auth.Token(token)
        self.g = Github(auth=auth, lazy=True)

    def test_connection(self, repo_name):
        try:
            repo = self.g.get_repo(repo_name)
            print(f"Successfully connected to {repo_name}")
        except Exception as e:
            print(f"Error connecting to {repo_name}: {e}")
            return False
        return True
    
    def get_pull_requests(self, repo_name, limit=50):        
        repo = self.g.get_repo(repo_name)
        # Ordenar pelas mais recentes ajuda a ter um diagnóstico do estado atual do time
        pulls = repo.get_pulls(state='closed', sort='created', direction='desc')[:limit] # Complexidade é alta

        pulls_merged = []

        for pull in pulls:
            if pull.merged:
                # Criamos um dicionário simples com o que o metrics.py realmente usa
                pulls_merged.append({
                    "number": pull.number,
                    "created_at": pull.created_at,
                    "merged_at": pull.merged_at,
                    "files_changed": pull.changed_files,
                    "commits": pull.commits
                })

        return pulls_merged
                

if __name__ == "__main__":
    collector = GithubCollector()
    repo_to_test = os.getenv("GITHUB_REPO")
    if not repo_to_test:
        raise ValueError("GITHUB_REPO environment variable is not set")
    collector.test_connection(repo_to_test)