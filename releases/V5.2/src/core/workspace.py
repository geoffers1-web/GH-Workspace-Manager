from pathlib import Path

REQUIRED_FOLDERS = [
    "Archive",
    "Assets",
    "Documentation",
    "GitHub",
    "Logs",
    "Projects",
    "Releases",
    "Resources",
    "Scripts",
    "Templates",
]

class WorkspaceManager:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path).expanduser()

    def exists(self):
        return self.workspace_path.exists()

    def required_folders(self):
        return [self.workspace_path / folder for folder in REQUIRED_FOLDERS]

    def folder_status(self):
        status = []
        for folder in REQUIRED_FOLDERS:
            path = self.workspace_path / folder
            status.append({
                "name": folder,
                "path": str(path),
                "exists": path.exists()
            })
        return status

    def missing_folders(self):
        return [item for item in self.folder_status() if not item["exists"]]

    def create_missing_folders(self):
        created = []
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        for item in self.missing_folders():
            path = Path(item["path"])
            path.mkdir(parents=True, exist_ok=True)
            created.append(str(path))
        return created

    def health_summary(self):
        if not self.exists():
            return "Workspace folder does not exist."
        missing = self.missing_folders()
        if missing:
            return f"Workspace needs attention: {len(missing)} required folder(s) missing."
        return "Workspace looks healthy."
