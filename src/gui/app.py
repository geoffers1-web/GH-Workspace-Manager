
import tkinter as tk
from tkinter import ttk

PAGES=[
"Dashboard","Workspace","Projects","Git","Knowledge Base",
"Documentation","Backup Pro","Templates","Settings","Logs"
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GH Workspace Manager V4.0")
        self.geometry("1200x760")

        sidebar=ttk.Frame(self,padding=8)
        sidebar.pack(side="left",fill="y")

        content=ttk.Frame(self,padding=8)
        content.pack(side="right",fill="both",expand=True)

        self.title_lbl=ttk.Label(content,font=("TkDefaultFont",18,"bold"))
        self.title_lbl.pack(anchor="w")

        self.body=tk.Text(content)
        self.body.pack(fill="both",expand=True)

        for p in PAGES:
            ttk.Button(sidebar,text=p,width=24,
                       command=lambda n=p:self.show(n)).pack(pady=2)

        self.show("Dashboard")

    def show(self,name):
        self.title_lbl.config(text=name)
        self.body.delete("1.0","end")
        self.body.insert("end",
            f"{name}\n\n"
            "Professional module scaffold.\n\n"
            "Planned functionality:\n"
            "- Workspace management\n"
            "- Validation\n"
            "- Git/GitHub\n"
            "- Documentation\n"
            "- Knowledge Base\n"
            "- Backup Pro integration\n"
            "- Plugin support\n")

def run():
    App().mainloop()
