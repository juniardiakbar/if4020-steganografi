import tkinter as tk
from src.gui.app import App

if __name__ == '__main__':
    app = App()
    app.geometry('{}x{}'.format(800, 600))
    app.mainloop()
