import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.audio.extractor import Extractor
from src.helper.file import File


class AudioExtractForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Steganografi Extract Audio')

        self.render_file_frame()
        self.render_key_frame()
        self.render_output_frame()
        self.render_execute_frame()

    def initialize(self):
        self.TITLE_ROW = 0
        self.FILE_ROW = 1
        self.KEY_ROW = 2
        self.OUTPUT_ROW = 3
        self.EXECUTE_ROW = 4

        self.DEFAULT_OUT_FILENAME = 'extract_result'

        self.audio_dir = tk.StringVar()
        self.audio_dir.set('')

        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)

    def render_file_frame(self):
        file_frame = hg.create_frame(self, self.FILE_ROW + 1)

        hg.create_label(file_frame, 'Audio', 0, 0)
        hg.create_label(file_frame, self.audio_dir, 0, 1, fix_text=False)
        hg.create_button(file_frame, 'Choose',
                         lambda: self.load_audio_file(), 1, 0)

        hg.create_button(file_frame, 'Play Sound',
                         lambda: hg.play_audio_file(self.audio_dir.get()), 1, 1)

    def render_key_frame(self):
        key_frame = hg.create_frame(self, self.KEY_ROW + 1)

        hg.create_label(key_frame, 'Stegano Key:', 0, 0)
        self.key_entry = hg.create_entry(key_frame, "", 1, 0)

    def render_output_frame(self):
        output_frame = hg.create_frame(self, self.OUTPUT_ROW + 1)

        hg.create_label(output_frame, 'Output file\'s name:', 0, 0)
        self.output_name = hg.create_entry(
            output_frame, self.DEFAULT_OUT_FILENAME, 1, 0)

    def render_execute_frame(self):
        execute_frame = hg.create_frame(self, self.EXECUTE_ROW + 1)

        hg.create_button(execute_frame, 'Execute',
                         lambda: self.execute(), 0, 0)

        hg.create_button(execute_frame, 'Back',
                         lambda: self.controller.show_frame("StartPage"), 0, 1)

    def load_audio_file(self):
        dialog = fd.askopenfilename(
            filetypes=((".WAV Audio", "*.wav"),)
        )
        self.audio_dir.set(dialog)

    def execute(self):
        print('Extract Started!')
        print('> Audio dir:', self.audio_dir.get())
        print('> Key:', self.key_entry.get())

        file_dir = self.audio_dir.get()
        key = self.key_entry.get()
        output_filename = self.output_name.get()

        try:
            if file_dir == '' or key == '' or output_filename == '':
                return

            extract = Extractor(file_dir, key)
            extract.extract_messages()
            extract.parse_message()

            file_name = "output/" + output_filename + "." + extract.extension
            output_file = File(file_name)
            byte = extract.get_secret_message()
            output_file.write_files(byte)

            print('Extraction Finished!')

            title = "Finish Extract Secret Message from Audio"
            self.controller.show_end_frame(title, "None", file_name, 0)

        except Exception as e:
            print("Error occured while extract secret message")
            print(e)
