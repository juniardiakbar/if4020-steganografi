import tkinter as tk
import tkinter.filedialog as tkfd

from src.audio.insertor import Inserter
from src.helper.file import File


class AudioInsertionForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.RANDOM_FRAME = 0
        self.TITLE_ROW = 0
        self.COVER_FILE_ROW = 1
        self.SECRET_MESSAGE_ROW = 2
        self.KEY_ENTRY_ROW = 3
        self.OPTIONS_ROW = 4
        self.SAVEAS_ROW = 5
        self.EXECUTE_ROW = 6

        self.DEFAULT_OUT_FILENAME = 'video_insertion_result'

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text='Steganografi Audio',
            font='none 24 bold'
        )
        heading.place(relx=0.25, rely=0.1, anchor=tk.W)

        self.cover_file_dir = tk.StringVar()
        self.cover_file_dir.set('')
        self.is_mono = False
        self.render_cover_file_frame()

        self.secret_message_dir = tk.StringVar()
        self.secret_message_dir.set('')
        self.render_secret_message_frame()

        key_frame = tk.Frame(self)
        key_frame.configure(bg='white')
        key_frame.place(
            relx=0.25,
            rely=(0.1 * (self.KEY_ENTRY_ROW + 1)),
            anchor=tk.W
        )

        key_label = tk.Label(
            master=key_frame,
            text='Stegano Key:',
            bg="white",
            fg="black"
        )
        key_label.grid(row=0, column=0, sticky=tk.W)
        self.key_entry = tk.Entry(master=key_frame, bg="white", fg="black")
        self.key_entry.grid(row=0, column=1)

        self.use_encryption = tk.IntVar()
        self.use_encryption.set(0)
        self.random = tk.IntVar()
        self.random.set(0)

        self.options_buttons = {}
        self.render_lsb_options_frame()
        self.render_output_frame()
        self.render_execute_frame()

    def render_cover_file_frame(self):
        ca_dialog_frame = tk.Frame(self)
        ca_dialog_frame.configure(bg='white')
        ca_dialog_frame.place(
            relx=0.25,
            rely=(0.1 * (self.COVER_FILE_ROW + 1)),
            anchor=tk.W
        )

        label_text = tk.Label(
            master=ca_dialog_frame,
            text='Audio:',
            bg="white",
            fg="black"
        )
        label_text.grid(row=0, column=0, sticky=tk.W)

        cv_input_label = tk.Label(
            master=ca_dialog_frame,
            textvariable=self.cover_file_dir,
            bg="white",
            fg="black"
        )
        cv_input_label.grid(row=0, column=1, sticky=tk.W)

        pick_cv_button = tk.Button(
            master=ca_dialog_frame,
            text='Pilih',
            command=lambda: self.load_audio_file(),
            bg="white",
            fg="black"
        )
        pick_cv_button.grid(row=1, column=0, sticky=tk.W)

    def render_secret_message_frame(self):
        msg_dialog_frame = tk.Frame(self)
        msg_dialog_frame.configure(bg='white')
        msg_dialog_frame.place(
            relx=0.25,
            rely=(0.1 * (self.SECRET_MESSAGE_ROW + 1)),
            anchor=tk.W
        )

        label_text = tk.Label(
            master=msg_dialog_frame,
            text='Secret Message:',
            bg="white",
            fg="black"
        )
        label_text.grid(row=0, column=0, sticky=tk.W)

        msg_input_label = tk.Label(
            master=msg_dialog_frame,
            textvariable=self.secret_message_dir,
            bg="white",
            fg="black"
        )
        msg_input_label.grid(row=0, column=1, sticky=tk.W)

        pick_msg_button = tk.Button(
            master=msg_dialog_frame,
            text='Pilih',
            command=lambda: self.load_secret_message(),
            bg="white",
            fg="black"
        )
        pick_msg_button.grid(row=1, column=0, sticky=tk.W)

    def render_lsb_options_frame(self):
        option_frame = tk.Frame(self)
        option_frame.configure(bg='white')
        option_frame.place(
            relx=0.25,
            rely=(0.1 * (self.OPTIONS_ROW + 1)),
            anchor=tk.W
        )

        label_text = tk.Label(
            master=option_frame,
            text='Option:',
            bg="white",
            fg="black"
        )
        label_text.grid(row=0, column=0, sticky=tk.W)

        self.options_buttons['Encrypt'] = tk.Checkbutton(
            master=option_frame,
            text='Encrypt message',
            variable=self.use_encryption,
            bg="white",
            fg="black"
        )
        self.options_buttons['Random'] = tk.Checkbutton(
            master=option_frame,
            text='Random frame',
            variable=self.random,
            bg="white",
            fg="black"
        )
        self.options_buttons['Encrypt'].grid(row=1, column=0, sticky=tk.W)
        self.options_buttons['Random'].grid(row=1, column=1, sticky=tk.W)

    def render_output_frame(self):
        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)

        saveas_dialog_frame = tk.Frame(self)
        saveas_dialog_frame.configure(bg='white')
        saveas_dialog_frame.place(
            relx=0.25,
            rely=(0.1 * (self.SAVEAS_ROW + 1)),
            anchor=tk.W
        )

        label_text = tk.Label(
            master=saveas_dialog_frame,
            text='Nama file output::',
            bg="white",
            fg="black"
        )
        label_text.grid(row=0, column=0, sticky=tk.W)

        self.saveas_entry = tk.Entry(master=saveas_dialog_frame)
        self.saveas_entry.configure(bg="white", fg="black")
        self.saveas_entry.grid(row=1, column=0, sticky=tk.W)
        self.saveas_entry.insert(tk.END, self.DEFAULT_OUT_FILENAME)
        tk.Label(
            master=saveas_dialog_frame,
            text='.wav',
            bg="white",
            fg="black"
        ).grid(row=1, column=1, sticky=tk.W)

    def render_execute_frame(self):
        execute_frame = tk.Frame(self)
        execute_frame.configure(bg='white')
        execute_frame.place(
            relx=0.25,
            rely=(0.1 * (self.EXECUTE_ROW + 1)),
            anchor=tk.W
        )

        execute_button = tk.Button(
            master=execute_frame,
            text='Execute',
            command=lambda: self.execute(
                self.key_entry.get(), self.saveas_entry.get())
        )

        execute_button.grid(row=0, column=0)
        return_button = tk.Button(
            master=execute_frame,
            text='Kembali',
            command=lambda: self.controller.show_frame("StartPage")
        )
        return_button.grid(row=0, column=1)

    def load_audio_file(self):
        self.cover_file_dir.set(tkfd.askopenfilename(filetypes=(
            (".WAV Audio", "*.wav"),
        )))

    def load_secret_message(self):
        self.secret_message_dir.set(tkfd.askopenfilename())

    def execute(self, key, output_filename):
        if self.cover_file_dir.get() == '' or self.secret_message_dir.get() == '' or key == '' or output_filename == '':
            return

        file_dir = self.cover_file_dir.get()
        secret_message_dir = self.secret_message_dir.get()

        insert = Inserter(file_dir, secret_message_dir, key)

        frame_modified = insert.insert_message(
            randomize=self.random.get(),
            encrypted=self.use_encryption.get(),
        )

        output_file = File(output_filename)
        output_file.write_audio_file(frame_modified, insert.params)

        print('Insertion Finished!')
