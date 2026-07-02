from pathlib import Path


class SearchService:
    def __init__(self, workspace_path: Path, logger=None):
        self.workspace_path = Path(workspace_path)
        self.logger = logger

    def search(self, query):
        query = query.strip().lower()
        results = []

        if not query or not self.workspace_path.exists():
            return results

        for path in self.workspace_path.rglob("*"):
            try:
                name_match = query in path.name.lower()
                extension_match = query.startswith(".") and path.suffix.lower() == query
                todo_match = False

                if path.is_file() and path.suffix.lower() in [".py", ".md", ".txt", ".sh"]:
                    try:
                        text = path.read_text(encoding="utf-8", errors="ignore").lower()
                        todo_match = query in text
                    except Exception:
                        todo_match = False

                if name_match or extension_match or todo_match:
                    results.append({
                        "name": path.name,
                        "path": str(path),
                        "type": "Folder" if path.is_dir() else "File",
                        "extension": path.suffix.lower() if path.is_file() else "",
                    })

            except Exception:
                continue

        if self.logger:
            self.logger.info(f"Search completed for query: {query} | Results: {len(results)}")

        return results
