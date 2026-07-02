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
BUILDER_VERSION = "2.0"
WINDOW_TITLE = f"{APP_NAME} {APP_RELEASE}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
""")

write("Builder/builder.py", """
from pathlib import Path
from datetime import datetime
import importlib.util
import json
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = PROJECT_ROOT / "releases"
SETTINGS_FILE = PROJECT_ROOT / "src" / "config" / "settings.py"


class GHWorkspaceBuilder:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.releases_dir = RELEASES_DIR
        self.settings = self.load_settings()

    def load_settings(self):
        defaults = {
            "APP_NAME": "GH Workspace Manager",
            "APP_VERSION": "Unknown",
            "APP_RELEASE": "VUnknown",
            "BUILDER_VERSION": "2.0",
        }

        if not SETTINGS_FILE.exists():
            return defaults

        try:
            spec = importlib.util.spec_from_file_location("settings", SETTINGS_FILE)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return {
                "APP_NAME": getattr(module, "APP_NAME", defaults["APP_NAME"]),
                "APP_VERSION": getattr(module, "APP_VERSION", defaults["APP_VERSION"]),
                "APP_RELEASE": getattr(module, "APP_RELEASE", f'V{getattr(module, "APP_VERSION", "Unknown")}'),
                "BUILDER_VERSION": getattr(module, "BUILDER_VERSION", defaults["BUILDER_VERSION"]),
            }
        except Exception:
            return defaults

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
                self.validate_structure()
            elif choice == "2":
                self.verify_imports()
            elif choice == "3":
                self.git_status()
            elif choice == "4":
                self.create_release_snapshot()
            elif choice == "5":
                self.list_releases()
            elif choice == "6":
                self.launch_application()
            elif choice == "7":
                self.pre_release_health_check()
            elif choice == "8":
                self.show_release_manifest()
            elif choice == "0":
                print("Exiting Builder.")
                break
            else:
                print("Invalid option.")

    def required_paths(self):
        return [
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

    def validate_structure(self):
        print()
        print("Validating project structure...")

        missing = []

        for path in self.required_paths():
            full_path = self.project_root / path
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

    def verify_imports(self):
        print()
        print("Verifying Python imports...")

        python_files = list((self.project_root / "src").rglob("*.py"))

        if not python_files:
            print("No Python files found.")
            return False

        failed = []

        for file_path in python_files:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(file_path)],
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

        print()
        if failed:
            print("Import verification failed.")
            return False

        print("Import verification successful.")
        return True

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

    def git_is_clean(self):
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.project_root,
            text=True,
            capture_output=True
        )

        return result.stdout.strip() == ""

    def create_release_snapshot(self):
        release_name = self.settings["APP_RELEASE"]
        release_dir = self.releases_dir / release_name
        release_dir.mkdir(parents=True, exist_ok=True)

        items = [
            "src",
            "docs",
            "Builder",
            "README.md",
            "CHANGELOG.md",
        ]

        print()
        print(f"Creating release snapshot: {release_name}")

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
            "name": self.settings["APP_NAME"],
            "app_version": self.settings["APP_VERSION"],
            "release": release_name,
            "builder_version": self.settings["BUILDER_VERSION"],
            "entry_point": "src/main.py",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "created_by": "GH Workspace Builder",
            "includes": items,
            "git_clean_at_creation": self.git_is_clean(),
        }

        manifest_path = release_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=4), encoding="utf-8")

        notes_path = release_dir / "RELEASE_NOTES.md"
        if not notes_path.exists():
            notes_path.write_text(
                f"# {release_name} Release Notes\\n\\nRelease snapshot created by GH Workspace Builder.\\n",
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
            manifest_path = self.releases_dir / release / "manifest.json"
            if manifest_path.exists():
                try:
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    created_at = manifest.get("created_at", "unknown date")
                    builder_version = manifest.get("builder_version", "unknown builder")
                    print(f"- {release} | {created_at} | Builder {builder_version}")
                except Exception:
                    print(f"- {release}")
            else:
                print(f"- {release}")

    def launch_application(self):
        print()
        print("Launching GH Workspace Manager...")

        subprocess.run(
            [sys.executable, "src/main.py"],
            cwd=self.project_root
        )

    def pre_release_health_check(self):
        print()
        print("Running pre-release health check...")
        print()

        structure_ok = self.validate_structure()
        imports_ok = self.verify_imports()
        git_clean = self.git_is_clean()

        print()
        print("Pre-release summary:")
        print(f"Structure ............. {'OK' if structure_ok else 'FAILED'}")
        print(f"Imports ............... {'OK' if imports_ok else 'FAILED'}")
        print(f"Git working tree ...... {'Clean' if git_clean else 'Changes pending'}")
        print(f"Target release ........ {self.settings['APP_RELEASE']}")

        if structure_ok and imports_ok:
            print()
            print("Health check passed.")
            if not git_clean:
                print("Note: Git has uncommitted changes. This is normal before committing the new release.")
        else:
            print()
            print("Health check failed.")

    def show_release_manifest(self):
        release_name = self.settings["APP_RELEASE"]
        manifest_path = self.releases_dir / release_name / "manifest.json"

        print()
        if not manifest_path.exists():
            print(f"No manifest found for {release_name}. Create a release snapshot first.")
            return

        print(manifest_path.read_text(encoding="utf-8"))


def main():
    builder = GHWorkspaceBuilder()
    builder.menu()


if __name__ == "__main__":
    main()
""")

write("docs/releases/V5.3_RELEASE_NOTES.md", """
# V5.3 Release Notes

V5.3 upgrades GH Workspace Builder to Builder V2.0.

Added:
- Automatic application version detection
- Automatic release snapshot naming
- Builder version metadata
- Timestamped manifest generation
- Pre-release health check
- Release manifest viewer
- Improved release listing
- Builder folder included in release snapshots
""")

write("docs/developer/V5.3_DEVELOPER_GUIDE.md", """
# V5.3 Developer Guide

## Builder V2.0

Run:

python Builder/builder.py

Builder V2.0 reads metadata from:

src/config/settings.py

The following values are used:

- APP_NAME
- APP_VERSION
- APP_RELEASE
- BUILDER_VERSION

## Recommended release workflow

1. Run the application
2. Test the new version
3. Run Builder
4. Run pre-release health check
5. Create release snapshot automatically
6. List releases
7. Commit and push
""")

write("docs/user/V5.3_USER_GUIDE.md", """
# V5.3 User Guide

## Builder V2.0

Run:

python Builder/builder.py

New options:

- Create release snapshot automatically
- Pre-release health check
- Show release manifest

You no longer need to manually type V5.3 when creating the release snapshot.
""")

write("docs/roadmap/V5.3_ROADMAP.md", """
# Roadmap

## Completed in V5.3

- Builder V2.0
- Automatic release detection
- Pre-release checks
- Release manifest viewer

## Next

- V5.4 Search & Indexing
- V5.5 Documentation Manager
- V5.6 Backup & Restore
- V6.0 Professional Workspace Suite
""")

write("docs/V5.3_TEST_CHECKLIST.md", """
# V5.3 Test Checklist

Run:

python build_v5_3.py
python src/main.py
python Builder/builder.py

## Application

- App opens as V5.3
- Dashboard works
- Git Manager works
- Workspace Scanner works
- Health Center works
- Project Explorer works
- Theme toggle works
- Theme persists after reopening

## Builder V2.0

- Builder opens as V2.0
- Builder displays application version V5.3
- Option 1 validates structure
- Option 2 verifies imports
- Option 3 shows Git status
- Option 4 creates releases/V5.3 automatically
- Option 5 lists releases with metadata
- Option 7 runs pre-release health check
- Option 8 shows V5.3 manifest
- Option 0 exits
""")

write("README.md", """
# GH Workspace Manager

Current Version: V5.3 - GH Workspace Builder 2.0

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
- Health Center
- Project Explorer
- Release package structure
- GH Workspace Builder 2.0
- Versioned documentation

## Run Application

python src/main.py

## Run Builder

python Builder/builder.py
""")

write("CHANGELOG.md", """
# Changelog

## V5.3 - GH Workspace Builder 2.0

Added:
- Automatic version detection
- Automatic release snapshot naming
- Timestamped manifests
- Builder version metadata
- Pre-release health check
- Release manifest viewer
- Improved release list
- Builder included in release snapshots

## V5.2 - Project Explorer

Added:
- ProjectService
- Project Explorer page
- Project Explorer plugin
- Project discovery
- Project details panel
- Project health status

## V5.1 - System Information & Health Center

Added:
- SystemInfoService
- Health Center page
- Health Center plugin
- Health check report
- Versioned documentation
""")

print()
print("V5.3 GH Workspace Builder 2.0 installed successfully.")
print("Next run: python src/main.py")
print("Then run: python Builder/builder.py")
