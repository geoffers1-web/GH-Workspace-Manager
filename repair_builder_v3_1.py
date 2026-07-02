from pathlib import Path

def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {p}")

write("run_builder.py", """
from Builder.builder import main

if __name__ == "__main__":
    main()
""")

write("Builder/builder.py", """
from pathlib import Path
import json
import shutil
import subprocess
import sys
from datetime import datetime
import importlib.util

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = PROJECT_ROOT / "releases"
SETTINGS_FILE = PROJECT_ROOT / "src" / "config" / "settings.py"

REQUIRED_PATHS = [
    "src/main.py",
    "src/config/settings.py",
    "src/gui/app.py",
    "src/services/project_service.py",
    "src/plugins/project_plugin.py",
    "README.md",
    "CHANGELOG.md",
]

SNAPSHOT_ITEMS = ["src", "docs", "Builder", "README.md", "CHANGELOG.md"]


def pause():
    input("\\nPress Enter to return to menu...")


def load_settings():
    defaults = {
        "APP_NAME": "GH Workspace Manager",
        "APP_VERSION": "5.3",
        "APP_RELEASE": "V5.3",
        "BUILDER_VERSION": "3.1",
    }

    try:
        spec = importlib.util.spec_from_file_location("settings", SETTINGS_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        app_version = getattr(module, "APP_VERSION", defaults["APP_VERSION"])

        return {
            "APP_NAME": getattr(module, "APP_NAME", defaults["APP_NAME"]),
            "APP_VERSION": app_version,
            "APP_RELEASE": getattr(module, "APP_RELEASE", f"V{app_version}"),
            "BUILDER_VERSION": "3.1",
        }
    except Exception as error:
        print(f"Settings load warning: {error}")
        return defaults


def validate_structure():
    print("\\nValidating project structure...\\n", flush=True)
    missing = []

    for item in REQUIRED_PATHS:
        path = PROJECT_ROOT / item
        if path.exists():
            print(f"OK      {item}", flush=True)
        else:
            print(f"MISSING {item}", flush=True)
            missing.append(item)

    print()
    print("Validation successful." if not missing else f"Validation failed: {len(missing)} missing item(s).", flush=True)
    return not missing


def verify_imports():
    print("\\nVerifying Python imports...\\n", flush=True)
    failed = []

    for file_path in sorted((PROJECT_ROOT / "src").rglob("*.py")):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file_path)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
        )

        rel = file_path.relative_to(PROJECT_ROOT)

        if result.returncode == 0:
            print(f"OK      {rel}", flush=True)
        else:
            print(f"FAILED  {rel}", flush=True)
            print(result.stderr, flush=True)
            failed.append(rel)

    print()
    print("Import verification successful." if not failed else "Import verification failed.", flush=True)
    return not failed


def show_git_status():
    print("\\nGit status:\\n", flush=True)
    result = subprocess.run(
        ["git", "status"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )
    print(result.stdout or result.stderr or "No Git output returned.", flush=True)


def git_is_clean():
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() == ""


def create_release_snapshot(settings):
    release_name = settings["APP_RELEASE"]
    release_dir = RELEASES_DIR / release_name

    print(f"\\nCreating release snapshot: {release_name}\\n", flush=True)
    release_dir.mkdir(parents=True, exist_ok=True)

    for item in SNAPSHOT_ITEMS:
        source = PROJECT_ROOT / item
        dest = release_dir / item

        if not source.exists():
            print(f"Skipped missing: {item}", flush=True)
            continue

        if source.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(source, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)

        print(f"Copied: {item}", flush=True)

    manifest = {
        "name": settings["APP_NAME"],
        "app_version": settings["APP_VERSION"],
        "release": release_name,
        "builder_version": settings["BUILDER_VERSION"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "created_by": "GH Workspace Builder V3.1",
        "entry_point": "src/main.py",
        "includes": SNAPSHOT_ITEMS,
        "git_clean_at_creation": git_is_clean(),
    }

    (release_dir / "manifest.json").write_text(json.dumps(manifest, indent=4), encoding="utf-8")

    notes = release_dir / "RELEASE_NOTES.md"
    if not notes.exists():
        notes.write_text(f"# {release_name} Release Notes\\n\\nCreated by GH Workspace Builder V3.1.\\n", encoding="utf-8")

    print(f"\\nRelease snapshot created at: {release_dir}", flush=True)


def list_releases():
    print("\\nAvailable releases:\\n", flush=True)

    if not RELEASES_DIR.exists():
        print("No releases folder found.", flush=True)
        return

    releases = sorted([p for p in RELEASES_DIR.iterdir() if p.is_dir()])

    if not releases:
        print("No releases found.", flush=True)
        return

    for release in releases:
        manifest = release / "manifest.json"
        if manifest.exists():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                print(f"- {release.name} | {data.get('created_at', 'unknown date')} | Builder {data.get('builder_version', 'unknown')}", flush=True)
            except Exception:
                print(f"- {release.name}", flush=True)
        else:
            print(f"- {release.name} | no manifest", flush=True)


def show_manifest(settings):
    release_name = settings["APP_RELEASE"]
    manifest = RELEASES_DIR / release_name / "manifest.json"

    print(f"\\nManifest for {release_name}:\\n", flush=True)

    if not manifest.exists():
        print("No manifest found. Run option 4 first.", flush=True)
        return

    print(manifest.read_text(encoding="utf-8"), flush=True)


def health_check(settings):
    print("\\nRunning pre-release health check...", flush=True)
    structure_ok = validate_structure()
    imports_ok = verify_imports()
    clean = git_is_clean()

    print("\\nPre-release summary:")
    print(f"Structure ............. {'OK' if structure_ok else 'FAILED'}")
    print(f"Imports ............... {'OK' if imports_ok else 'FAILED'}")
    print(f"Git working tree ...... {'Clean' if clean else 'Changes pending'}")
    print(f"Target release ........ {settings['APP_RELEASE']}")
    print("Health check passed." if structure_ok and imports_ok else "Health check failed.", flush=True)


def launch_app():
    subprocess.run([sys.executable, "src/main.py"], cwd=PROJECT_ROOT)


def main():
    settings = load_settings()

    while True:
        print()
        print("========================================")
        print(f"GH Workspace Builder V{settings['BUILDER_VERSION']}")
        print("========================================")
        print(f"Application : {settings['APP_NAME']}")
        print(f"Version     : {settings['APP_RELEASE']}")
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

        choice = input("\\nSelect option: ").strip()

        if choice == "1":
            validate_structure()
            pause()
        elif choice == "2":
            verify_imports()
            pause()
        elif choice == "3":
            show_git_status()
            pause()
        elif choice == "4":
            create_release_snapshot(settings)
            pause()
        elif choice == "5":
            list_releases()
            pause()
        elif choice == "6":
            launch_app()
        elif choice == "7":
            health_check(settings)
            pause()
        elif choice == "8":
            show_manifest(settings)
            pause()
        elif choice == "0":
            print("Exiting Builder.")
            break
        else:
            print("Invalid option.")
            pause()


if __name__ == "__main__":
    main()
""")

print()
print("Builder V3.1 repair installed.")
print("Run: python run_builder.py")
