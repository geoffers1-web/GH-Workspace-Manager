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
            f"# {release_name} Release Notes\n\nRelease snapshot created by GH Workspace Builder V3.0.\n",
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
