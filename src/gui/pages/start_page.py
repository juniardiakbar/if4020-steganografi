import tkinter as tk


class StartPage(tk.Frame):
    def donothing(self):
        filewin = tk.Toplevel(self.master)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text='Tugas Besar 1: Steganografi',
            font='none 24 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        menu_elements = [
            {"text": "Hide mesage to picture", "command": self.donothing},
            {"text": "Extract mesage to picture", "command": self.donothing},
            {"text": "Hide mesage to audio",
                "command": lambda: controller.show_frame("AudioInsertionForm")},
            {"text": "Extract mesage to audio", "command": self.donothing},
            {"text": "Hide mesage to video", "command": self.donothing},
            {"text": "Extract mesage to video", "command": self.donothing}
        ]

        index = 0
        for el in menu_elements:
            button = tk.Button(
                self,
                bg='white',
                fg='black',
                text=el["text"],
                command=el["command"],
                width=50,
                height=2
            )
            button.place(relx=0.5, rely=0.1*(index+2), anchor=tk.CENTER)
            index += 1
