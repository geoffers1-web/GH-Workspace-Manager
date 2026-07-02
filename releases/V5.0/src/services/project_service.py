from pathlib import Path
from datetime import datetime


class ProjectService:
    def __init__(self, workspace_path: Path, logger=None):
        self.workspace_path = Path(workspace_path)
        self.logger = logger

    def discover_projects(self):
        projects = []

        if not self.workspace_path.exists():
            return projects

        for path in self.workspace_path.rglob("*"):
            if not path.is_dir():
                continue

            is_git = (path / ".git").exists()
            has_python = any(path.glob("*.py")) or (path / "src").exists()
            has_readme = (path / "README.md").exists()
            has_gitignore = (path / ".gitignore").exists()

            if is_git or has_python or has_readme:
                projects.append({
                    "name": path.name,
                    "path": str(path),
                    "is_git": is_git,
                    "has_python": has_python,
                    "has_readme": has_readme,
                    "has_gitignore": has_gitignore,
                    "last_modified": self.get_last_modified(path),
                    "health": self.get_project_health(is_git, has_readme, has_gitignore),
                })

        projects.sort(key=lambda item: item["name"].lower())

        if self.logger:
            self.logger.info(f"Project discovery completed: {len(projects)} projects found")

        return projects

    def get_last_modified(self, path):
        try:
            timestamp = path.stat().st_mtime
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "Unknown"

    def get_project_health(self, is_git, has_readme, has_gitignore):
        if is_git and has_readme and has_gitignore:
            return "Healthy"
        if is_git and has_readme:
            return "Needs .gitignore"
        if is_git and has_gitignore:
            return "Needs README"
        if is_git:
            return "Needs documentation"
        return "Local project"
