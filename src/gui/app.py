import tkinter as tk
from tkinter import ttk
def run():
    r=tk.Tk()
    r.title("GH Workspace Manager 4.0.1")
    r.geometry("1000x700")
    ttk.Label(r,text="GH Workspace Manager",font=("TkDefaultFont",18,"bold")).pack(pady=20)
    ttk.Label(r,text="Professional GitHub Foundation").pack()
    r.mainloop()
