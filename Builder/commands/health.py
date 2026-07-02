from pathlib import Path

from Builder.commands.validate import validate_structure
from Builder.commands.imports import verify_imports
from Builder.commands.git_tools import git_is_clean


def pre_release_health_check(project_root: Path, settings: dict):
    print()
    print("Running pre-release health check...")

    structure_ok = validate_structure(project_root)
    imports_ok = verify_imports(project_root)
    git_clean = git_is_clean(project_root)

    print()
    print("Pre-release summary:")
    print(f"Structure ............. {'OK' if structure_ok else 'FAILED'}")
    print(f"Imports ............... {'OK' if imports_ok else 'FAILED'}")
    print(f"Git working tree ...... {'Clean' if git_clean else 'Changes pending'}")
    print(f"Target release ........ {settings['APP_RELEASE']}")

    if structure_ok and imports_ok:
        print()
        print("Health check passed.")
        if not git_clean:
            print("Note: Git has uncommitted changes. This is normal before committing the new release.")
        return True

    print()
    print("Health check failed.")
    return False
