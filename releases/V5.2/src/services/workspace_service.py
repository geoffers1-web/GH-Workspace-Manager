from pathlib import Path


class WorkspaceService:
    def __init__(self, workspace_path: Path, logger=None):
        self.workspace_path = Path(workspace_path)
        self.logger = logger

    def scan_workspace(self):
        results = {
            "workspace_path": str(self.workspace_path),
            "total_folders": 0,
            "total_files": 0,
            "git_repositories": 0,
            "python_files": 0,
            "bash_scripts": 0,
            "markdown_docs": 0,
            "pdf_files": 0,
            "image_files": 0,
            "projects_missing_readme": [],
            "projects_missing_gitignore": [],
        }

        if not self.workspace_path.exists():
            return results

        for path in self.workspace_path.rglob("*"):
            if path.is_dir():
                results["total_folders"] += 1

                if (path / ".git").exists():
                    results["git_repositories"] += 1

                    if not (path / "README.md").exists():
                        results["projects_missing_readme"].append(str(path))

                    if not (path / ".gitignore").exists():
                        results["projects_missing_gitignore"].append(str(path))

            elif path.is_file():
                results["total_files"] += 1
                suffix = path.suffix.lower()

                if suffix == ".py":
                    results["python_files"] += 1
                elif suffix == ".sh":
                    results["bash_scripts"] += 1
                elif suffix in [".md", ".txt", ".rst"]:
                    results["markdown_docs"] += 1
                elif suffix == ".pdf":
                    results["pdf_files"] += 1
                elif suffix in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
                    results["image_files"] += 1

        if self.logger:
            self.logger.info("Workspace scan completed")

        return results
