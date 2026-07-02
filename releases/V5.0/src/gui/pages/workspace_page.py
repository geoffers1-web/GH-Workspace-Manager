import tkinter as tk
from tkinter import filedialog

from services.workspace_service import WorkspaceService
from core.paths import PROJECT_ROOT


class WorkspacePage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.workspace_path = PROJECT_ROOT

        self.title = tk.Label(self, text="Workspace Scanner & Project Explorer", font=("Arial", 18, "bold"))
        self.title.pack(pady=20)

        self.path_label = tk.Label(self, text=f"Workspace: {self.workspace_path}", font=("Arial", 10))
        self.path_label.pack(pady=5)

        self.choose_button = tk.Button(self, text="Choose Workspace Folder", command=self.choose_workspace)
        self.choose_button.pack(pady=5)

        self.scan_button = tk.Button(self, text="Scan Workspace", command=self.scan_workspace)
        self.scan_button.pack(pady=5)

        self.output = tk.Text(self, height=24, width=100)
        self.output.pack(pady=10)

    def choose_workspace(self):
        selected = filedialog.askdirectory(title="Choose GH Workspace Folder")
        if selected:
            self.workspace_path = selected
            self.path_label.configure(text=f"Workspace: {self.workspace_path}")

    def scan_workspace(self):
        service = WorkspaceService(self.workspace_path, self.app_state.logger)
        results = service.scan_workspace()
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.format_report(results))

    def format_report(self, results):
        missing_readme = "\n".join(results["projects_missing_readme"][:10]) or "None"
        missing_gitignore = "\n".join(results["projects_missing_gitignore"][:10]) or "None"

        return f'''GH Workspace Scan Report

Workspace:
{results["workspace_path"]}

Summary:
Folders ................ {results["total_folders"]}
Files .................. {results["total_files"]}
Git Repositories ....... {results["git_repositories"]}
Python Files ........... {results["python_files"]}
Bash Scripts ........... {results["bash_scripts"]}
Documents .............. {results["markdown_docs"]}
PDF Files .............. {results["pdf_files"]}
Image Files ............ {results["image_files"]}

Projects Missing README.md:
{missing_readme}

Projects Missing .gitignore:
{missing_gitignore}
'''

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])

        for widget in [self.title, self.path_label]:
            widget.configure(bg=theme["content_bg"], fg=theme["fg"])

        for button in [self.choose_button, self.scan_button]:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        self.output.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )
