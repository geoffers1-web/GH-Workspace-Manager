from pathlib import Path

ROOT = Path(__file__).parent

files = {
    "docs/releases/V6.0_RELEASE_NOTES.md": """# V6.0 Release Notes

## Release Focus

V6.0 begins the professional desktop framework phase.

## Added

- Professional application menu bar.
- Status bar foundation.
- Help menu integration.
- Framework preparation for future File, View, Tools, and Help actions.

## Status

GH Workspace is now moving from foundation releases into feature-driven desktop application development.
""",

    "docs/V6.0_TEST_CHECKLIST.md": """# V6.0 Test Checklist

## Build

- [ ] Run `python build_v6_0.py`

## Application

- [ ] Run `python src/main.py`
- [ ] Confirm application opens without errors
- [ ] Confirm menu bar appears
- [ ] Confirm Help > About opens the About dialog
- [ ] Confirm status bar appears at bottom
- [ ] Confirm sidebar buttons still work
- [ ] Confirm Toggle Theme still works

## Repository

- [ ] Run `git status`
- [ ] Commit and push after successful test
"""
}

for path, content in files.items():
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

print("V6.0 documentation files created successfully.")
