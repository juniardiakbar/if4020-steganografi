import tkinter as tk


class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='Tugas Besar 1: Steganografi', font='none 24 bold').grid(
            row=0, columnspan=2)

        ins_pict_button = tk.Button(
            self,
            text='Hide Message to Picture',
            command=lambda: master.open_hide_audio_form(),
        )
        ext_pict_button = tk.Button(
            self,
            text='Ekstract Message from Picture',
            command=lambda: master.open_extract_audio_form(),
        )
        ins_pict_button.grid(row=1, column=0)
        ext_pict_button.grid(row=1, column=1)

        ins_aud_button = tk.Button(
            self,
            text='Hide Message to Audio',
            command=lambda: master.open_hide_audio_form(),
        )
        ext_aud_button = tk.Button(
            self,
            text='Ekstract Message from Audio',
            command=lambda: master.open_extract_audio_form(),
        )
        ins_aud_button.grid(row=2, column=0)
        ext_aud_button.grid(row=2, column=1)

        ins_vid_button = tk.Button(
            self,
            text='Hide Message to Video',
            command=lambda: master.open_hide_vid_form()
        )
        ext_vid_button = tk.Button(
            self,
            text='Ekstract Message from Video',
            command=lambda: master.open_extract_vid_form()
        )

        ins_vid_button.grid(row=3, column=0)
        ext_vid_button.grid(row=3, column=1)

        exit_button = tk.Button(self, text='Exit', command=master.destroy)
        exit_button.grid(row=4, column=0, columnspan=2)
