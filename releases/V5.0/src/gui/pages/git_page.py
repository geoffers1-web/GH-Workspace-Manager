import tkinter as tk
from services.git_service import GitService
from core.paths import PROJECT_ROOT


class GitPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.git_service = GitService(PROJECT_ROOT)

        self.title = tk.Label(self, text="Git Manager", font=("Arial", 18, "bold"))
        self.title.pack(pady=20)

        self.status_button = tk.Button(self, text="Show Git Status", command=self.show_status)
        self.status_button.pack(pady=5)

        self.log_button = tk.Button(self, text="Show Recent Commits", command=self.show_log)
        self.log_button.pack(pady=5)

        self.output = tk.Text(self, height=20, width=100)
        self.output.pack(pady=10)

    def show_status(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.git_service.status())

    def show_log(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.git_service.log())

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])

        for button in [self.status_button, self.log_button]:
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
