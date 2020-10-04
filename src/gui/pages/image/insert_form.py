import cv2
import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.image.insertor import Inserter
from src.helper.file import File


class ImageInsertionForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Steganografi Insert Image')

        self.render_file_frame()
        self.render_message_frame()
        self.render_key_frame()
        self.render_options_frame()
        self.render_output_frame()
        self.render_execute_frame()

    def initialize(self):
        self.TITLE_ROW = 0
        self.FILE_ROW = 1
        self.MESSAGE_ROW = 2
        self.KEY_ROW = 3
        self.OPTIONS_ROW = 4
        self.OUTPUT_ROW = 5
        self.EXECUTE_ROW = 6

        self.DEFAULT_OUT_FILENAME = 'insert_result'

        self.encrypt = tk.IntVar()
        self.encrypt.set(0)
        self.random = tk.IntVar()
        self.random.set(0)

        self.output_ext = tk.StringVar()
        self.output_ext.set('bmp')

        self.image_dir = tk.StringVar()
        self.image_dir.set('')

        self.message_dir = tk.StringVar()
        self.message_dir.set('')

        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)

    def render_file_frame(self):
        file_frame = hg.create_frame(self, self.FILE_ROW + 1)

        hg.create_label(file_frame, 'Image', 0, 0)
        hg.create_label(file_frame, self.image_dir, 0, 1, fix_text=False)
        hg.create_button(file_frame, 'Choose',
                         lambda: self.load_image_file(), 1, 0)

        hg.create_button(file_frame, 'Preview Image',
                         lambda: hg.show_image_preview(self.image_dir.get()), 1, 1)

    def render_message_frame(self):
        msg_frame = hg.create_frame(self, self.MESSAGE_ROW + 1)

        hg.create_label(msg_frame, 'Secret Message', 0, 0)
        hg.create_label(msg_frame, self.message_dir, 0, 1, fix_text=False)
        hg.create_button(msg_frame, 'Choose',
                         lambda: self.load_secret_message(), 1, 0)

    def render_key_frame(self):
        key_frame = hg.create_frame(self, self.KEY_ROW + 1)

        hg.create_label(key_frame, 'Stegano Key:', 0, 0)
        self.key_entry = hg.create_entry(key_frame, "", 1, 0)

    def render_options_frame(self):
        option_frame = hg.create_frame(self, self.OPTIONS_ROW + 1)

        hg.create_label(option_frame, 'Option:', 0, 0)
        hg.create_check_button(
            option_frame, 'Encrypt Message', self.encrypt, 1, 0)
        hg.create_check_button(
            option_frame, 'Random Frame', self.random, 1, 1)

    def render_output_frame(self):
        output_frame = hg.create_frame(self, self.OUTPUT_ROW + 1)

        hg.create_label(output_frame, 'Output file\'s name:', 0, 0)
        hg.create_radio_button(
            output_frame, 'bmp', self.output_ext, 1, 1)
        hg.create_radio_button(
            output_frame, 'png', self.output_ext, 1, 2)
        self.output_name = hg.create_entry(
            output_frame, self.DEFAULT_OUT_FILENAME, 1, 0)

    def render_execute_frame(self):
        execute_frame = hg.create_frame(self, self.EXECUTE_ROW + 1)

        hg.create_button(execute_frame, 'Execute',
                         lambda: self.execute(), 0, 0)

        hg.create_button(execute_frame, 'Back',
                         lambda: self.controller.show_frame("StartPage"), 0, 1)

    def load_image_file(self):
        dialog = fd.askopenfilename(
            filetypes=(("Image File", ('.bmp', '.png')),)
        )
        self.image_dir.set(dialog)

    def load_secret_message(self):
        self.message_dir.set(fd.askopenfilename())

    def execute(self):
        print('Insertion Started!')
        print('> Image dir:', self.image_dir.get())
        print('> Message dir:', self.message_dir.get())
        print('> Key:', self.key_entry.get())
        print('> Random:', self.random.get())
        print('> Encrypt:', self.output_name.get())
        print('> Output ext:', self.output_ext.get())

        file_dir = self.image_dir.get()
        message_dir = self.message_dir.get()
        key = self.key_entry.get()
        output_filename = self.output_name.get()
        output_fileext = self.output_ext.get()

        if file_dir == '' or message_dir == '' or key == '' or output_filename == '':
            return

        insert = Inserter(file_dir, message_dir, key)

        image_modified = insert.insert_message(
            randomize=self.random.get(),
            encrypted=self.encrypt.get(),
        )

        file_name = "output/" + output_filename + "." + output_fileext
        output_file = File(file_name)
        output_file.write_image_file(image_modified)

        print('Insertion Finished!')

        image = cv2.imread(file_dir)
        cv2.imshow('Original Image', image_modified)
        cv2.imshow('Steganography Image', image_modified)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        title = "Finish Insert Secret Message to Image"
        self.controller.show_end_frame(title, "Image", file_name)
