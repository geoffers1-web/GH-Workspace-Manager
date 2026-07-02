import tkinter as tk
from core.paths import APP_LOG_FILE


class DashboardPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state

        self.title = tk.Label(
            self,
            text="Dashboard & Workspace Health",
            font=("Arial", 18, "bold")
        )
        self.title.pack(pady=20)

        self.message = tk.Label(
            self,
            text="GH Workspace Manager professional modular architecture is running.",
            font=("Arial", 12)
        )
        self.message.pack(pady=10)

        self.log_info = tk.Label(
            self,
            text=f"Log file: {APP_LOG_FILE}",
            font=("Arial", 10)
        )
        self.log_info.pack(pady=10)

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.message.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.log_info.configure(bg=theme["content_bg"], fg=theme["fg"])
