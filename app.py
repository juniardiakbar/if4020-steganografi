import tkinter as tk
from src.gui.app import App

if __name__ == '__main__':
    root = tk.Tk()
    gui = App(root)
    root.mainloop()
