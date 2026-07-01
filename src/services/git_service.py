import subprocess
from pathlib import Path


class GitService:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    def run_git_command(self, args):
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                text=True,
                capture_output=True,
                check=False
            )
            return result.stdout.strip() or result.stderr.strip()
        except Exception as error:
            return f"Git error: {error}"

    def status(self):
        return self.run_git_command(["status"])

    def log(self):
        return self.run_git_command(["log", "--oneline", "-10"])
