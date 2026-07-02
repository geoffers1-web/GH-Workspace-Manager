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
        if not self.repo_path.exists():
            return False, "Repository path does not exist."

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

    def remote_list(self):
        ok, output = self.run_git(["remote", "-v"])
        if ok:
            return output if output else "No remote configured"
        return output

    def status_short(self):
        ok, output = self.run_git(["status", "--short"])
        if ok:
            return output if output else "Working tree clean"
        return output

    def status_full(self):
        ok, output = self.run_git(["status"])
        if ok:
            return output
        return output

    def log_recent(self, count=8):
        ok, output = self.run_git(["log", "--oneline", "--decorate", f"-{count}"])
        if ok:
            return output if output else "No commits found"
        return output

    def add_all(self):
        return self.run_git(["add", "."])

    def commit(self, message):
        message = message.strip()
        if not message:
            return False, "Commit message cannot be empty."
        return self.run_git(["commit", "-m", message])

    def push(self):
        return self.run_git(["push"])

    def pull(self):
        return self.run_git(["pull", "--ff-only"])

    def status_summary(self):
        if not self.git_available():
            return "Git is not installed."
        if not self.repo_path.exists():
            return "Repository path does not exist."
        if not self.is_repository():
            return "This folder is not a Git repository."

        return (
            f"Branch: {self.current_branch()}\n\n"
            f"Status:\n{self.status_short()}\n\n"
            f"Remote:\n{self.remote_list()}\n\n"
            f"Recent commits:\n{self.log_recent()}"
        )
