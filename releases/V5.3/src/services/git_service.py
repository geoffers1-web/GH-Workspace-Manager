import subprocess
from pathlib import Path
from core.logger import app_logger


class GitService:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.logger = app_logger

    def run_git_command(self, args):
        command = "git " + " ".join(args)
        self.logger.info(f"Running command: {command}")

        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                text=True,
                capture_output=True,
                check=False
            )

            output = result.stdout.strip() or result.stderr.strip()

            if result.returncode == 0:
                self.logger.info(f"Command completed: {command}")
            else:
                self.logger.warning(f"Command warning/error: {output}")

            return output

        except Exception as error:
            self.logger.exception("Git command failed")
            return f"Git error: {error}"

    def status(self):
        return self.run_git_command(["status"])

    def log(self):
        return self.run_git_command(["log", "--oneline", "-10"])
