from pathlib import Path
import subprocess
import sys


def verify_imports(project_root: Path):
    print()
    print("Verifying Python imports...")

    python_files = list((project_root / "src").rglob("*.py"))

    if not python_files:
        print("No Python files found.")
        return False

    failed = []

    for file_path in python_files:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file_path)],
            cwd=project_root,
            text=True,
            capture_output=True
        )

        rel_path = file_path.relative_to(project_root)

        if result.returncode == 0:
            print(f"OK      {rel_path}")
        else:
            print(f"FAILED  {rel_path}")
            print(result.stderr)
            failed.append(rel_path)

    print()

    if failed:
        print("Import verification failed.")
        return False

    print("Import verification successful.")
    return True
