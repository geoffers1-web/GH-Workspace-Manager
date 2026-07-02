import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from core.paths import PROJECT_ROOT
from services.search_service import SearchService


class SearchPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.workspace_path = PROJECT_ROOT
        self.results = []

        self.title = tk.Label(self, text="Search & Indexing", font=("Arial", 18, "bold"))
        self.title.pack(pady=15)

        self.path_label = tk.Label(self, text=f"Workspace: {self.workspace_path}", font=("Arial", 10))
        self.path_label.pack(pady=5)

        self.controls = tk.Frame(self)
        self.controls.pack(pady=5)

        self.query_entry = tk.Entry(self.controls, width=40)
        self.query_entry.pack(side="left", padx=5)

        self.search_button = tk.Button(self.controls, text="Search", command=self.run_search)
        self.search_button.pack(side="left", padx=5)

        self.choose_button = tk.Button(self.controls, text="Choose Workspace", command=self.choose_workspace)
        self.choose_button.pack(side="left", padx=5)

        self.output = tk.Text(self, height=26, width=105)
        self.output.pack(padx=10, pady=10)

        self.output.insert(tk.END, "Search examples:\n\n.py\nREADME\nTODO\nFIXME\nproject name\n")

    def choose_workspace(self):
        selected = filedialog.askdirectory(title="Choose Workspace Folder")
        if selected:
            self.workspace_path = Path(selected)
            self.path_label.configure(text=f"Workspace: {self.workspace_path}")

    def run_search(self):
        query = self.query_entry.get()
        service = SearchService(self.workspace_path, self.app_state.logger)
        self.results = service.search(query)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"Search query: {query}\n")
        self.output.insert(tk.END, f"Results found: {len(self.results)}\n\n")

        for item in self.results[:200]:
            self.output.insert(tk.END, f"{item['type']}: {item['name']}\n")
            self.output.insert(tk.END, f"{item['path']}\n\n")

        if len(self.results) > 200:
            self.output.insert(tk.END, "Only first 200 results shown.\n")

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.path_label.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.controls.configure(bg=theme["content_bg"])

        for button in [self.search_button, self.choose_button]:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        self.query_entry.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )

        self.output.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )
