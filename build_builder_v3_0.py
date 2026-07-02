from pathlib import Path

def write(path, content):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {file_path}")

write("src/config/settings.py", """
APP_NAME = "GH Workspace Manager"
APP_VERSION = "5.3"
APP_RELEASE = "V5.3"
BUILDER_VERSION = "3.0"
WINDOW_TITLE = f"{APP_NAME} {APP_RELEASE}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
""")

write("Builder/__init__.py", "")

write("Builder/services/__init__.py", "")

write("Builder/commands/__init__.py", "")

write("Builder/services/settings_service.py", """
from pathlib import Path
import importlib.util


class SettingsService:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.settings_file = project_root / "src" / "config" / "settings.py"

    def load(self):
        defaults = {
            "APP_NAME": "GH Workspace Manager",
            "APP_VERSION": "Unknown",
            "APP_RELEASE": "VUnknown",
            "BUILDER_VERSION": "3.0",
        }

        if not self.settings_file.exists():
            return defaults

        try:
            spec = importlib.util.spec_from_file_location("settings", self.settings_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            app_version = getattr(module, "APP_VERSION", defaults["APP_VERSION"])

            return {
                "APP_NAME": getattr(module, "APP_NAME", defaults["APP_NAME"]),
                "APP_VERSION": app_version,
                "APP_RELEASE": getattr(module, "APP_RELEASE", f"V{app_version}"),
                "BUILDER_VERSION": getattr(module, "BUILDER_VERSION", defaults["BUILDER_VERSION"]),
            }
        except Exception as error:
            print(f"Could not load settings: {error}")
            return defaults
""")

write("Builder/commands/validate.py", """
from pathlib import Path


REQUIRED_PATHS = [
    "src/main.py",
    "src/config/settings.py",
    "src/config/config_manager.py",
    "src/core/app_state.py",
    "src/core/logger.py",
    "src/core/plugin_manager.py",
    "src/gui/app.py",
    "src/gui/theme_manager.py",
    "src/gui/pages/dashboard_page.py",
    "src/gui/pages/git_page.py",
    "src/gui/pages/workspace_page.py",
    "src/gui/pages/health_page.py",
    "src/gui/pages/project_page.py",
    "src/services/git_service.py",
    "src/services/workspace_service.py",
    "src/services/system_info_service.py",
    "src/services/project_service.py",
    "src/plugins/base_plugin.py",
    "src/plugins/dashboard_plugin.py",
    "src/plugins/git_plugin.py",
    "src/plugins/workspace_plugin.py",
    "src/plugins/health_plugin.py",
    "src/plugins/project_plugin.py",
    "README.md",
    "CHANGELOG.md",
]


def validate_structure(project_root: Path):
    print()
    print("Validating project structure...")

    missing = []

    for path in REQUIRED_PATHS:
        full_path = project_root / path
        if full_path.exists():
            print(f"OK      {path}")
        else:
            print(f"MISSING {path}")
            missing.append(path)

    print()

    if missing:
        print(f"Validation failed. Missing items: {len(missing)}")
        return False

    print("Validation successful.")
    return True
""")

write("Builder/commands/imports.py", """
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
""")

write("Builder/commands/git_tools.py", """
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
""")

write("Builder/commands/releases.py", """
from pathlib import Path
from datetime import datetime
import json
import shutil

from Builder.commands.git_tools import git_is_clean


SNAPSHOT_ITEMS = [
    "src",
    "docs",
    "Builder",
    "README.md",
    "CHANGELOG.md",
]


def create_release_snapshot(project_root: Path, settings: dict):
    releases_dir = project_root / "releases"
    release_name = settings["APP_RELEASE"]
    release_dir = releases_dir / release_name

    print()
    print(f"Creating release snapshot: {release_name}")

    release_dir.mkdir(parents=True, exist_ok=True)

    for item in SNAPSHOT_ITEMS:
        source = project_root / item
        destination = release_dir / item

        if not source.exists():
            print(f"Skipped missing: {item}")
            continue

        if source.is_dir():
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        print(f"Copied: {item}")

    manifest = {
        "name": settings["APP_NAME"],
        "app_version": settings["APP_VERSION"],
        "release": settings["APP_RELEASE"],
        "builder_version": settings["BUILDER_VERSION"],
        "entry_point": "src/main.py",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "created_by": "GH Workspace Builder V3.0",
        "includes": SNAPSHOT_ITEMS,
        "git_clean_at_creation": git_is_clean(project_root),
    }

    manifest_path = release_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=4), encoding="utf-8")

    notes_path = release_dir / "RELEASE_NOTES.md"
    if not notes_path.exists():
        notes_path.write_text(
            f"# {release_name} Release Notes\\n\\nRelease snapshot created by GH Workspace Builder V3.0.\\n",
            encoding="utf-8"
        )

    print()
    print(f"Release snapshot created at: {release_dir}")
    return release_dir


def list_releases(project_root: Path):
    releases_dir = project_root / "releases"

    print()
    print("Available releases:")

    if not releases_dir.exists():
        print("No releases folder found.")
        return

    releases = sorted([path for path in releases_dir.iterdir() if path.is_dir()])

    if not releases:
        print("No releases found.")
        return

    for release_dir in releases:
        manifest_path = release_dir / "manifest.json"

        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                created_at = manifest.get("created_at", "unknown date")
                builder_version = manifest.get("builder_version", "unknown builder")
                print(f"- {release_dir.name} | {created_at} | Builder {builder_version}")
            except Exception:
                print(f"- {release_dir.name}")
        else:
            print(f"- {release_dir.name}")


def show_release_manifest(project_root: Path, settings: dict):
    release_name = settings["APP_RELEASE"]
    manifest_path = project_root / "releases" / release_name / "manifest.json"

    print()

    if not manifest_path.exists():
        print(f"No manifest found for {release_name}. Create a release snapshot first.")
        return

    print(manifest_path.read_text(encoding="utf-8"))
""")

write("Builder/commands/health.py", """
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
""")

write("Builder/commands/launcher.py", """
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
""")

write("Builder/builder.py", """
from pathlib import Path

from Builder.services.settings_service import SettingsService
from Builder.commands.validate import validate_structure
from Builder.commands.imports import verify_imports
from Builder.commands.git_tools import show_git_status
from Builder.commands.releases import (
    create_release_snapshot,
    list_releases,
    show_release_manifest,
)
from Builder.commands.health import pre_release_health_check
from Builder.commands.launcher import launch_application


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GHWorkspaceBuilder:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.settings = SettingsService(PROJECT_ROOT).load()

    def menu(self):
        while True:
            print()
            print("========================================")
            print(f"GH Workspace Builder V{self.settings['BUILDER_VERSION']}")
            print("========================================")
            print(f"Application : {self.settings['APP_NAME']}")
            print(f"Version     : {self.settings['APP_RELEASE']}")
            print("========================================")
            print("1. Validate project structure")
            print("2. Verify Python imports")
            print("3. Show Git status")
            print("4. Create release snapshot automatically")
            print("5. List releases")
            print("6. Launch application")
            print("7. Pre-release health check")
            print("8. Show release manifest")
            print("0. Exit")
            print()

            choice = input("Select option: ").strip()

            if choice == "1":
                validate_structure(self.project_root)
            elif choice == "2":
                verify_imports(self.project_root)
            elif choice == "3":
                show_git_status(self.project_root)
            elif choice == "4":
                create_release_snapshot(self.project_root, self.settings)
            elif choice == "5":
                list_releases(self.project_root)
            elif choice == "6":
                launch_application(self.project_root)
            elif choice == "7":
                pre_release_health_check(self.project_root, self.settings)
            elif choice == "8":
                show_release_manifest(self.project_root, self.settings)
            elif choice == "0":
                print("Exiting Builder.")
                break
            else:
                print("Invalid option.")


def main():
    builder = GHWorkspaceBuilder()
    builder.menu()


if __name__ == "__main__":
    main()
""")

write("docs/releases/V5.3_BUILDER_V3_RELEASE_NOTES.md", """
# V5.3 Builder V3.0 Release Notes

Builder V3.0 refactors the GH Workspace Builder into a modular architecture.

Added:

- Builder/services/settings_service.py
- Builder/commands/validate.py
- Builder/commands/imports.py
- Builder/commands/git_tools.py
- Builder/commands/releases.py
- Builder/commands/health.py
- Builder/commands/launcher.py

Improved:

- Cleaner menu controller
- Reliable release snapshot creation
- Reliable release listing
- Reliable manifest viewing
- Easier future Builder upgrades
""")

write("docs/developer/V5.3_BUILDER_V3_DEVELOPER_GUIDE.md", """
# Builder V3.0 Developer Guide

The Builder now follows a modular command architecture.

## Structure

Builder/
- builder.py
- services/settings_service.py
- commands/validate.py
- commands/imports.py
- commands/git_tools.py
- commands/releases.py
- commands/health.py
- commands/launcher.py

## Design Rule

The main builder.py file should only manage the menu.

Command logic should live in Builder/commands/.

Reusable data loading should live in Builder/services/.
""")

write("docs/V5.3_BUILDER_V3_TEST_CHECKLIST.md", """
# Builder V3.0 Test Checklist

Run:

python build_builder_v3_0.py
python Builder/builder.py

Test:

- Option 1 validates structure
- Option 2 verifies imports
- Option 3 shows Git status
- Option 4 creates releases/V5.3
- Option 5 lists releases
- Option 7 runs health check
- Option 8 shows manifest after option 4
- Option 0 exits
""")

print()
print("Builder V3.0 modular architecture installed successfully.")
print("Next run: python Builder/builder.py")
