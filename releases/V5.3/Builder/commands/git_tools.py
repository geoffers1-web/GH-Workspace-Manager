from pathlib import Path
import subprocess


def show_git_status(project_root: Path):
    print()
    print("Git status:")

    result = subprocess.run(
        ["git", "status"],
        cwd=project_root,
        text=True,
        capture_output=True
    )

    print(result.stdout or result.stderr)


def git_is_clean(project_root: Path):
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=project_root,
        text=True,
        capture_output=True
    )

    return result.stdout.strip() == ""
