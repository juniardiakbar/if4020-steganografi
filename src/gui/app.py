import tkinter as tk
import src.gui.pages.mainmenu as mainmenu


class App(tk.Tk):
    def __init__(self, master, width='800', height='600', resizable=True):
        self.master = master
        master.title('Tugas Besar 1')
        master.geometry('{}x{}'.format(str(width), str(height)))
        master.configure(bg='white')

        self.open_main_menu()

    def donothing(self):
        filewin = tk.Toplevel(self.master)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()

    def open_main_menu(self):
        heading = tk.Label(
            self.master,
            bg="white",
            fg="black",
            text='Tugas Besar 1: Steganografi',
            font='none 24 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        menu_elements = [
            {"text": "Hide mesage to picture", "command": self.donothing},
            {"text": "Extract mesage to picture", "command": self.donothing},
            {"text": "Hide mesage to audio", "command": self.donothing},
            {"text": "Extract mesage to audio", "command": self.donothing},
            {"text": "Hide mesage to video", "command": self.donothing},
            {"text": "Extract mesage to video", "command": self.donothing}
        ]

        index = 0
        for el in menu_elements:
            button = tk.Button(
                self.master,
                bg='white',
                fg='black',
                text=el["text"],
                command=el["command"],
                width=50,
                height=2
            )
            button.place(relx=0.5, rely=0.1*(index+2), anchor=tk.CENTER)
            index += 1

        # hide_menu = tk.Menu(menu_bar, tearoff=0)
        # for el in hide_menu_elements:
        #     hide_menu.add_command(label=el["text"], command=el["command"])

        # hide_menu.add_separator()
        # menu_bar.add_cascade(label="Hide message", menu=hide_menu)

        # extract_menu = tk.Menu(menu_bar, tearoff=0)
        # for el in extract_menu_elements:
        #     extract_menu.add_command(label=el["text"], command=el["command"])

        # extract_menu.add_separator()
        # menu_bar.add_cascade(label="Extract message", menu=extract_menu)

        # self.master.config(menu=menu_bar)
