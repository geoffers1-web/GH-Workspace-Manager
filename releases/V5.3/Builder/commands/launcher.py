from pathlib import Path
import subprocess
import sys


def launch_application(project_root: Path):
    print()
    print("Launching GH Workspace Manager...")

    subprocess.run(
        [sys.executable, "src/main.py"],
        cwd=project_root
    )
