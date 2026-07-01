import tkinter as tk
from core.paths import APP_LOG_FILE


class DashboardPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state

        title = tk.Label(
            self,
            text="Dashboard & Workspace Health",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        message = tk.Label(
            self,
            text="GH Workspace Manager professional modular architecture is running.",
            font=("Arial", 12)
        )
        message.pack(pady=10)

        log_info = tk.Label(
            self,
            text=f"Log file: {APP_LOG_FILE}",
            font=("Arial", 10)
        )
        log_info.pack(pady=10)
