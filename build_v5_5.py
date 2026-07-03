from pathlib import Path

ROOT = Path(__file__).parent

files = {
    "src/core/app_metadata.py": '''"""
Application metadata for GH Workspace.

This file is the single source of truth for application identity.
"""

APP_NAME = "GH Workspace"
APP_VERSION = "5.5"
APP_RELEASE = "V5.5"
APP_AUTHOR = "Geoffrey D Hinds"
APP_DESCRIPTION = "Professional desktop workspace manager for GitHub-based projects."


def get_window_title() -> str:
    return f"{APP_NAME} {APP_RELEASE}"
''',

    "docs/releases/V5.5_RELEASE_NOTES.md": """# V5.5 Release Notes

## Release Focus

V5.5 is an application identity stabilization release.

## Added

- Added central application metadata module.
- Added single source of truth for app name, version, release, author, and description.
- Prepared the project for future Help/About dialog and professional branding.

## Status

GH Workspace continues as a working professional modular desktop application.
""",

    "docs/V5.5_TEST_CHECKLIST.md": """# V5.5 Test Checklist

## Build

- [ ] Run `python build_v5_5.py`
- [ ] Confirm V5.5 files are created

## Application

- [ ] Run `python src/main.py`
- [ ] Confirm application opens without errors
- [ ] Confirm existing V5.4 functionality still works

## Repository

- [ ] Run `git status`
- [ ] Confirm only expected V5.5 files changed
- [ ] Commit and push after successful test
"""
}

for path, content in files.items():
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

print("V5.5 files created successfully.")
