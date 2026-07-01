import shutil
import subprocess
from pathlib import Path

class GitTools:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path).expanduser()

    def git_available(self):
        return shutil.which("git") is not None

    def is_repository(self):
        return (self.repo_path / ".git").exists()

    def run_git(self, args):
        if not self.git_available():
            return False, "Git is not installed."
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                text=True,
                capture_output=True,
                check=False,
            )
            output = result.stdout.strip() or result.stderr.strip()
            return result.returncode == 0, output
        except Exception as exc:
            return False, str(exc)

    def current_branch(self):
        ok, output = self.run_git(["branch", "--show-current"])
        if ok and output:
            return output
        return "Not available"

    def status_short(self):
        ok, output = self.run_git(["status", "--short"])
        if ok:
            return output if output else "Working tree clean"
        return output

    def status_summary(self):
        if not self.git_available():
            return "Git is not installed."
        if not self.repo_path.exists():
            return "Repository path does not exist."
        if not self.is_repository():
            return "This folder is not a Git repository."
        return f"Branch: {self.current_branch()}\nStatus: {self.status_short()}"
