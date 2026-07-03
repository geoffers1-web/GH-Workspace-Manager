import tkinter as tk
from tkinter import ttk

from config.settings import load_settings, save_settings


class PreferencesDialog(tk.Toplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)

        self.title("Preferences")
        self.geometry("360x260")
        self.resizable(False, False)

        self.on_save = on_save
        self.settings = load_settings()

        self.theme_var = tk.StringVar(value=self.settings.get("theme", "system"))
        self.startup_view_var = tk.StringVar(value=self.settings.get("startup_view", "dashboard"))
        self.show_status_bar_var = tk.BooleanVar(value=self.settings.get("show_status_bar", True))
        self.autosave_var = tk.BooleanVar(value=self.settings.get("autosave", True))

        self.build_ui()

        self.transient(parent)
        self.grab_set()

    def build_ui(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Theme").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Combobox(
            frame,
            textvariable=self.theme_var,
            values=["system", "light", "dark"],
            state="readonly"
        ).grid(row=0, column=1, pady=6)

        ttk.Label(frame, text="Startup View").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(
            frame,
            textvariable=self.startup_view_var,
            values=["dashboard", "projects", "recent"],
            state="readonly"
        ).grid(row=1, column=1, pady=6)

        ttk.Checkbutton(frame, text="Show status bar", variable=self.show_status_bar_var).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=6
        )

        ttk.Checkbutton(frame, text="Enable autosave", variable=self.autosave_var).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=6
        )

        buttons = ttk.Frame(frame)
        buttons.grid(row=4, column=0, columnspan=2, sticky="e", pady=(16, 0))

        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(buttons, text="Save", command=self.save).pack(side="right", padx=4)

    def save(self):
        self.settings["theme"] = self.theme_var.get()
        self.settings["startup_view"] = self.startup_view_var.get()
        self.settings["show_status_bar"] = self.show_status_bar_var.get()
        self.settings["autosave"] = self.autosave_var.get()

        save_settings(self.settings)

        if self.on_save:
            self.on_save(self.settings)

        self.destroy()
