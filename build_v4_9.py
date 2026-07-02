from pathlib import Path
import json
import shutil

VERSION = "V4.9"
RELEASE_DIR = Path("releases") / VERSION

FILES_TO_PACKAGE = [
    "src",
    "docs",
    "README.md",
    "CHANGELOG.md",
]

def copy_item(source, destination):
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        print(f"Skipped missing: {source}")
        return

    if source.is_dir():
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    print(f"Packaged: {source} -> {destination}")

def write(path, content):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {file_path}")

def main():
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)

    write("src/config/settings.py", '''
APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.9"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
''')

    write("docs/V4.9_RELEASE_PACKAGE_STRUCTURE.md", '''
# V4.9 Release Package Structure

This release introduces a professional release package structure.

## New Folder

releases/V4.9/

## Purpose

The releases folder stores complete version snapshots of the application.

Each release can contain:

- src/
- docs/
- README.md
- CHANGELOG.md
- RELEASE_NOTES.md
- manifest.json

## Why This Matters

This prepares GH Workspace Manager for the permanent GH Workspace Builder planned for V5.0.
''')

    write("docs/V4.9_TEST_CHECKLIST.md", '''
# V4.9 Test Checklist

- App opens as V4.9
- Dashboard works
- Git Manager works
- Workspace Scanner works
- Theme toggle works
- Theme is remembered after reopen
- releases/V4.9 folder exists
- releases/V4.9/manifest.json exists
- releases/V4.9/src exists
- releases/V4.9/docs exists
''')

    write("README.md", '''
# GH Workspace Manager

Current Version: V4.9 - Release Package Structure

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

## Run

python src/main.py
''')

    write("CHANGELOG.md", '''
# Changelog

## V4.9 - Release Package Structure

Added:
- releases/ folder structure
- V4.9 release package snapshot
- manifest.json release metadata
- V4.9 documentation
- V4.9 test checklist

## V4.8 - Workspace Scanner & Project Explorer

Added:
- Workspace Scanner plugin
- Workspace Scanner page
- Workspace scanning service
- Git repository detection
- File type counting
- Missing README.md detection
- Missing .gitignore detection
''')

    manifest = {
        "name": "GH Workspace Manager",
        "version": "4.9",
        "release": "V4.9",
        "description": "Release Package Structure",
        "entry_point": "src/main.py",
        "created_by": "GH Workspace Manager release builder",
        "includes": FILES_TO_PACKAGE,
        "next_milestone": "V5.0 GH Workspace Builder"
    }

    write(RELEASE_DIR / "manifest.json", json.dumps(manifest, indent=4))

    for item in FILES_TO_PACKAGE:
        copy_item(item, RELEASE_DIR / item)

    write(RELEASE_DIR / "RELEASE_NOTES.md", '''
# V4.9 Release Notes

V4.9 introduces the formal release package structure.

This prepares the project for V5.0, where a permanent GH Workspace Builder will install, verify, and manage future releases.
''')

    print()
    print("V4.9 Release Package Structure created successfully.")
    print("Next run: python src/main.py")

if __name__ == "__main__":
    main()
