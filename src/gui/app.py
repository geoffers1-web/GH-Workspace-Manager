import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from core.settings import SettingsManager
from core.workspace import WorkspaceManager
from core.git_tools import GitTools

class GHWorkspaceManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GH Workspace Manager V4.1")
        self.geometry("1180x720")
        self.minsize(980, 620)

        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load()
        self.workspace_path = tk.StringVar(value=self.settings["workspace_path"])

        self._build_layout()
        self.refresh_all()

    def _build_layout(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self, padding=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ttk.Frame(self, padding=14)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)

        ttk.Label(
            self.sidebar,
            text="GH Workspace\nManager",
            font=("TkDefaultFont", 16, "bold"),
            justify="center",
        ).pack(pady=(0, 18))

        ttk.Button(self.sidebar, text="Dashboard", width=24, command=self.show_dashboard).pack(pady=3)
        ttk.Button(self.sidebar, text="Workspace", width=24, command=self.show_workspace).pack(pady=3)
        ttk.Button(self.sidebar, text="Git Status", width=24, command=self.show_git).pack(pady=3)
        ttk.Button(self.sidebar, text="Refresh", width=24, command=self.refresh_all).pack(pady=(20, 3))

        self.page_title = ttk.Label(self.content, text="", font=("TkDefaultFont", 18, "bold"))
        self.page_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.body = ttk.Frame(self.content)
        self.body.grid(row=1, column=0, sticky="nsew")
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)

        self.status_bar = ttk.Label(self, text="Ready", anchor="w", padding=6)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def clear_body(self):
        for widget in self.body.winfo_children():
            widget.destroy()

    def set_status(self, text):
        self.status_bar.config(text=text)

    def get_workspace_manager(self):
        return WorkspaceManager(self.workspace_path.get())

    def get_git_tools(self):
        return GitTools(Path.cwd())

    def refresh_all(self):
        self.show_dashboard()
        self.set_status("Dashboard refreshed.")

    def show_dashboard(self):
        self.clear_body()
        self.page_title.config(text="Dashboard")

        workspace = self.get_workspace_manager()
        git = self.get_git_tools()

        summary_frame = ttk.LabelFrame(self.body, text="Workspace Summary", padding=12)
        summary_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(summary_frame, text="Workspace Path:", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(summary_frame, text=str(workspace.workspace_path)).grid(row=0, column=1, sticky="w", padx=8)

        ttk.Label(summary_frame, text="Health:", font=("TkDefaultFont", 10, "bold")).grid(row=1, column=0, sticky="w")
        ttk.Label(summary_frame, text=workspace.health_summary()).grid(row=1, column=1, sticky="w", padx=8)

        ttk.Label(summary_frame, text="Git Installed:", font=("TkDefaultFont", 10, "bold")).grid(row=2, column=0, sticky="w")
        ttk.Label(summary_frame, text="Yes" if git.git_available() else "No").grid(row=2, column=1, sticky="w", padx=8)

        ttk.Label(summary_frame, text="Application Repository:", font=("TkDefaultFont", 10, "bold")).grid(row=3, column=0, sticky="w")
        ttk.Label(summary_frame, text="Yes" if git.is_repository() else "No").grid(row=3, column=1, sticky="w", padx=8)

        folders_frame = ttk.LabelFrame(self.body, text="Required Workspace Folders", padding=12)
        folders_frame.pack(fill="both", expand=True)

        columns = ("Folder", "Status", "Path")
        tree = ttk.Treeview(folders_frame, columns=columns, show="headings", height=12)
        for column in columns:
            tree.heading(column, text=column)
        tree.column("Folder", width=180)
        tree.column("Status", width=100)
        tree.column("Path", width=620)

        for item in workspace.folder_status():
            tree.insert("", "end", values=(item["name"], "OK" if item["exists"] else "Missing", item["path"]))

        tree.pack(fill="both", expand=True)

    def show_workspace(self):
        self.clear_body()
        self.page_title.config(text="Workspace")

        frame = ttk.LabelFrame(self.body, text="Workspace Location", padding=12)
        frame.pack(fill="x", pady=(0, 12))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Path:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.workspace_path).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(frame, text="Browse", command=self.browse_workspace).grid(row=0, column=2)

        ttk.Button(frame, text="Save Workspace Path", command=self.save_workspace_path).grid(row=1, column=1, sticky="w", pady=8)
        ttk.Button(frame, text="Create Missing Folders", command=self.create_missing_folders).grid(row=1, column=2, pady=8)

        info = tk.Text(self.body, height=18, wrap="word")
        info.pack(fill="both", expand=True)
        info.insert("end", "Workspace Builder\n\n")
        info.insert("end", "Select your main GH Workspace folder, save it, and create the required standard folders.\n\n")
        info.insert("end", "Recommended structure:\n")
        for folder in WorkspaceManager(self.workspace_path.get()).required_folders():
            info.insert("end", f"- {folder}\n")
        info.config(state="disabled")

    def browse_workspace(self):
        selected = filedialog.askdirectory(title="Select GH Workspace Folder")
        if selected:
            self.workspace_path.set(selected)

    def save_workspace_path(self):
        self.settings["workspace_path"] = self.workspace_path.get()
        self.settings_manager.save(self.settings)
        self.set_status("Workspace path saved.")
        messagebox.showinfo("Saved", "Workspace path saved successfully.")

    def create_missing_folders(self):
        workspace = self.get_workspace_manager()
        created = workspace.create_missing_folders()
        if created:
            messagebox.showinfo("Folders Created", f"Created {len(created)} folder(s).")
            self.set_status(f"Created {len(created)} missing folder(s).")
        else:
            messagebox.showinfo("No Action Needed", "All required folders already exist.")
            self.set_status("All required folders already exist.")
        self.show_dashboard()

    def show_git(self):
        self.clear_body()
        self.page_title.config(text="Git Status")

        git = self.get_git_tools()

        frame = ttk.LabelFrame(self.body, text="Application Repository", padding=12)
        frame.pack(fill="both", expand=True)

        output = tk.Text(frame, wrap="word")
        output.pack(fill="both", expand=True)
        output.insert("end", "GH Workspace Manager Repository Status\n")
        output.insert("end", "=" * 45 + "\n\n")
        output.insert("end", f"Current folder: {Path.cwd()}\n\n")
        output.insert("end", git.status_summary() + "\n")
        output.config(state="disabled")

def run():
    app = GHWorkspaceManager()
    app.mainloop()
