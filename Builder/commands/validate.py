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
