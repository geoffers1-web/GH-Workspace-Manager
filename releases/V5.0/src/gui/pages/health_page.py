import subprocess
import sys
import tkinter as tk
from pathlib import Path

from core.paths import PROJECT_ROOT, APP_LOG_FILE
from services.system_info_service import SystemInfoService


class HealthPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.system_info = SystemInfoService(app_state)

        self.title = tk.Label(
            self,
            text="System Information & Health Center",
            font=("Arial", 18, "bold")
        )
        self.title.pack(pady=20)

        self.refresh_button = tk.Button(
            self,
            text="Run Health Check",
            command=self.refresh_report
        )
        self.refresh_button.pack(pady=5)

        self.import_button = tk.Button(
            self,
            text="Verify Imports",
            command=self.verify_imports
        )
        self.import_button.pack(pady=5)

        self.builder_button = tk.Button(
            self,
            text="Launch Builder",
            command=self.launch_builder
        )
        self.builder_button.pack(pady=5)

        self.output = tk.Text(self, height=24, width=100)
        self.output.pack(pady=10)

        self.refresh_report()

    def refresh_report(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.system_info.format_health_report())
        self.app_state.logger.info("Health check refreshed")

    def verify_imports(self):
        python_files = list((PROJECT_ROOT / "src").rglob("*.py"))
        output_lines = ["Python Import Verification", ""]

        failed = []

        for file_path in python_files:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(file_path)],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True
            )

            rel_path = file_path.relative_to(PROJECT_ROOT)

            if result.returncode == 0:
                output_lines.append(f"OK      {rel_path}")
            else:
                output_lines.append(f"FAILED  {rel_path}")
                output_lines.append(result.stderr)
                failed.append(rel_path)

        output_lines.append("")
        output_lines.append("Result: SUCCESS" if not failed else "Result: FAILED")

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n".join(output_lines))

    def launch_builder(self):
        builder_path = PROJECT_ROOT / "Builder" / "builder.py"

        if not builder_path.exists():
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Builder not found.")
            return

        subprocess.Popen(
            [sys.executable, str(builder_path)],
            cwd=PROJECT_ROOT
        )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Builder launch requested.")

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])

        for button in [self.refresh_button, self.import_button, self.builder_button]:
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
