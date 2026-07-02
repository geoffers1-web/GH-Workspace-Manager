import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from core.paths import PROJECT_ROOT
from services.project_service import ProjectService


class ProjectPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.workspace_path = PROJECT_ROOT
        self.projects = []

        self.title = tk.Label(self, text="Project Explorer", font=("Arial", 18, "bold"))
        self.title.pack(pady=15)

        self.path_label = tk.Label(self, text=f"Workspace: {self.workspace_path}", font=("Arial", 10))
        self.path_label.pack(pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        self.choose_button = tk.Button(
            self.button_frame,
            text="Choose Workspace",
            command=self.choose_workspace
        )
        self.choose_button.pack(side="left", padx=5)

        self.scan_button = tk.Button(
            self.button_frame,
            text="Discover Projects",
            command=self.discover_projects
        )
        self.scan_button.pack(side="left", padx=5)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.listbox = tk.Listbox(self.main_frame, width=40)
        self.listbox.pack(side="left", fill="both", expand=False)
        self.listbox.bind("<<ListboxSelect>>", self.show_selected_project)

        self.details = tk.Text(self.main_frame, height=24, width=70)
        self.details.pack(side="right", fill="both", expand=True, padx=10)

    def choose_workspace(self):
        selected = filedialog.askdirectory(title="Choose GH Workspace Folder")
        if selected:
            self.workspace_path = Path(selected)
            self.path_label.configure(text=f"Workspace: {self.workspace_path}")

    def discover_projects(self):
        service = ProjectService(self.workspace_path, self.app_state.logger)
        self.projects = service.discover_projects()

        self.listbox.delete(0, tk.END)
        self.details.delete("1.0", tk.END)

        for project in self.projects:
            self.listbox.insert(tk.END, project["name"])

        self.details.insert(tk.END, f"Projects found: {len(self.projects)}")

    def show_selected_project(self, event=None):
        selection = self.listbox.curselection()

        if not selection:
            return

        project = self.projects[selection[0]]
        report = self.format_project_details(project)

        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, report)

    def yes_no(self, value):
        return "Yes" if value else "No"

    def format_project_details(self, project):
        return f'''Project Details

Name:
{project["name"]}

Path:
{project["path"]}

Git Repository:
{self.yes_no(project["is_git"])}

Python Project:
{self.yes_no(project["has_python"])}

README.md:
{self.yes_no(project["has_readme"])}

.gitignore:
{self.yes_no(project["has_gitignore"])}

Last Modified:
{project["last_modified"]}

Health:
{project["health"]}
'''

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.path_label.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.button_frame.configure(bg=theme["content_bg"])
        self.main_frame.configure(bg=theme["content_bg"])

        for button in [self.choose_button, self.scan_button]:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        self.listbox.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"]
        )

        self.details.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )
