from pathlib import Path

def write(path, content):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {file_path}")

write("src/config/settings.py", """
APP_NAME = "GH Workspace Manager"
APP_VERSION = "5.0"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
""")

write("Builder/builder.py", """
from pathlib import Path
import json
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = PROJECT_ROOT / "releases"


class GHWorkspaceBuilder:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.releases_dir = RELEASES_DIR

    def menu(self):
        while True:
            print()
            print("========================================")
            print("GH Workspace Builder V1.0")
            print("========================================")
            print("1. Validate project structure")
            print("2. Verify Python imports")
            print("3. Show Git status")
            print("4. Create release snapshot")
            print("5. List releases")
            print("6. Launch application")
            print("0. Exit")
            print()

            choice = input("Select option: ").strip()

            if choice == "1":
                self.validate_structure()
            elif choice == "2":
                self.verify_imports()
            elif choice == "3":
                self.git_status()
            elif choice == "4":
                version = input("Release version, example V5.0: ").strip()
                self.create_release_snapshot(version)
            elif choice == "5":
                self.list_releases()
            elif choice == "6":
                self.launch_application()
            elif choice == "0":
                print("Exiting Builder.")
                break
            else:
                print("Invalid option.")

    def validate_structure(self):
        required_paths = [
            "src/main.py",
            "src/config/settings.py",
            "src/core/app_state.py",
            "src/core/logger.py",
            "src/core/plugin_manager.py",
            "src/gui/app.py",
            "src/gui/theme_manager.py",
            "src/gui/pages/dashboard_page.py",
            "src/gui/pages/git_page.py",
            "src/gui/pages/workspace_page.py",
            "src/services/git_service.py",
            "src/services/workspace_service.py",
            "src/plugins/base_plugin.py",
            "src/plugins/dashboard_plugin.py",
            "src/plugins/git_plugin.py",
            "src/plugins/workspace_plugin.py",
            "README.md",
            "CHANGELOG.md",
        ]

        print()
        print("Validating project structure...")

        missing = []

        for path in required_paths:
            full_path = self.project_root / path
            if full_path.exists():
                print(f"OK      {path}")
            else:
                print(f"MISSING {path}")
                missing.append(path)

        if missing:
            print()
            print("Validation failed.")
            print(f"Missing items: {len(missing)}")
        else:
            print()
            print("Validation successful.")

    def verify_imports(self):
        print()
        print("Verifying Python imports...")

        command = [sys.executable, "-m", "py_compile"]

        python_files = list((self.project_root / "src").rglob("*.py"))

        if not python_files:
            print("No Python files found.")
            return

        failed = []

        for file_path in python_files:
            result = subprocess.run(
                command + [str(file_path)],
                cwd=self.project_root,
                text=True,
                capture_output=True
            )

            rel_path = file_path.relative_to(self.project_root)

            if result.returncode == 0:
                print(f"OK      {rel_path}")
            else:
                print(f"FAILED  {rel_path}")
                print(result.stderr)
                failed.append(rel_path)

        if failed:
            print()
            print("Import verification failed.")
        else:
            print()
            print("Import verification successful.")

    def git_status(self):
        print()
        print("Git status:")
        result = subprocess.run(
            ["git", "status"],
            cwd=self.project_root,
            text=True,
            capture_output=True
        )
        print(result.stdout or result.stderr)

    def create_release_snapshot(self, version):
        if not version:
            print("No version supplied.")
            return

        release_dir = self.releases_dir / version
        release_dir.mkdir(parents=True, exist_ok=True)

        items = [
            "src",
            "docs",
            "README.md",
            "CHANGELOG.md",
        ]

        print()
        print(f"Creating release snapshot: {version}")

        for item in items:
            source = self.project_root / item
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
            "name": "GH Workspace Manager",
            "release": version,
            "entry_point": "src/main.py",
            "created_by": "GH Workspace Builder V1.0",
            "includes": items,
        }

        manifest_path = release_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=4), encoding="utf-8")

        notes_path = release_dir / "RELEASE_NOTES.md"
        if not notes_path.exists():
            notes_path.write_text(
                f"# {version} Release Notes\\n\\nRelease snapshot created by GH Workspace Builder.\\n",
                encoding="utf-8"
            )

        print()
        print(f"Release snapshot created at: {release_dir}")

    def list_releases(self):
        print()
        print("Available releases:")

        if not self.releases_dir.exists():
            print("No releases folder found.")
            return

        releases = sorted([path.name for path in self.releases_dir.iterdir() if path.is_dir()])

        if not releases:
            print("No releases found.")
            return

        for release in releases:
            print(f"- {release}")

    def launch_application(self):
        print()
        print("Launching GH Workspace Manager...")
        subprocess.run(
            [sys.executable, "src/main.py"],
            cwd=self.project_root
        )


def main():
    builder = GHWorkspaceBuilder()
    builder.menu()


if __name__ == "__main__":
    main()
""")

write("docs/V5.0_GH_WORKSPACE_BUILDER.md", """
# V5.0 GH Workspace Builder

V5.0 introduces the GH Workspace Builder.

The Builder is a companion tool for managing development, validation, and release snapshots.

## Location

Builder/builder.py

## Run

python Builder/builder.py

## Builder Features

- Validate project structure
- Verify Python imports
- Show Git status
- Create release snapshots
- List releases
- Launch application

## Why This Matters

Earlier versions used one-off build scripts.

From V5.0 onward, GH Workspace Builder becomes the reusable tool for managing future releases.
""")

write("docs/V5.0_TEST_CHECKLIST.md", """
# V5.0 Test Checklist

Run:

python build_v5_0.py
python src/main.py
python Builder/builder.py

## Application

- App opens as V5.0
- Dashboard works
- Git Manager works
- Workspace Scanner works
- Theme toggle works
- Theme persists after reopening

## Builder

- Builder menu opens
- Option 1 validates project structure
- Option 2 verifies Python imports
- Option 3 shows Git status
- Option 4 creates a release snapshot
- Option 5 lists releases
- Option 6 launches the application
- Option 0 exits Builder
""")

write("README.md", """
# GH Workspace Manager

Current Version: V5.0 - GH Workspace Builder

GH Workspace Manager is a modular desktop application for managing a GitHub-based local workspace.

## Features

- Modular architecture
- Configuration manager
- Logging framework
- Theme manager
- Plugin framework
- Dashboard
- Git Manager
- Workspace Scanner
- Release package structure
- GH Workspace Builder

## Run Application

python src/main.py

## Run Builder

python Builder/builder.py
""")

write("CHANGELOG.md", """
# Changelog

## V5.0 - GH Workspace Builder

Added:
- Builder/builder.py
- Project structure validation
- Python import verification
- Git status command
- Release snapshot creation
- Release listing
- Application launcher
- V5.0 documentation
- V5.0 test checklist

## V4.9 - Release Package Structure

Added:
- releases/ folder structure
- release package snapshots
- manifest.json release metadata

## V4.8 - Workspace Scanner & Project Explorer

Added:
- Workspace Scanner plugin
- Workspace Scanner page
- Workspace scanning service
""")

print()
print("V5.0 GH Workspace Builder installed successfully.")
print("Next run: python src/main.py")
print("Then run: python Builder/builder.py")
