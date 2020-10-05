import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.video.insertor import Inserter
from src.helper.video_file import *


class VideoInsertionForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Steganografi Insert Video')

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
        self.random_frame = tk.IntVar()
        self.random_frame.set(0)
        self.random_pixel = tk.IntVar()
        self.random_pixel.set(0)

        self.video_dir = tk.StringVar()
        self.video_dir.set('')

        self.message_dir = tk.StringVar()
        self.message_dir.set('')

        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)

    def render_file_frame(self):
        file_frame = hg.create_frame(self, self.FILE_ROW + 1)

        hg.create_label(file_frame, 'Video', 0, 0)
        hg.create_label(file_frame, self.video_dir, 0, 1, fix_text=False)
        hg.create_button(file_frame, 'Choose',
                         lambda: self.load_video_file(), 1, 0)
        hg.create_button(file_frame, 'Play Video',
                         lambda: hg.play_video_file(self.video_dir.get()), 1, 1)

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
            option_frame, 'Random Frame', self.random_frame, 1, 1)
        hg.create_check_button(
            option_frame, 'Random Pixel', self.random_pixel, 1, 2)

    def render_output_frame(self):
        output_frame = hg.create_frame(self, self.OUTPUT_ROW + 1)

        hg.create_label(output_frame, 'Output file\'s name:', 0, 0)
        hg.create_label(output_frame, '.avi', 1, 1)
        self.output_name = hg.create_entry(
            output_frame, self.DEFAULT_OUT_FILENAME, 1, 0)

    def render_execute_frame(self):
        execute_frame = hg.create_frame(self, self.EXECUTE_ROW + 1)

        hg.create_button(execute_frame, 'Execute',
                         lambda: self.execute(), 0, 0)

        hg.create_button(execute_frame, 'Back',
                         lambda: self.controller.show_frame("StartPage"), 0, 1)

    def load_video_file(self):
        dialog = fd.askopenfilename(
            filetypes=((".AVI Videos", "*.avi"),)
        )
        self.video_dir.set(dialog)

    def load_secret_message(self):
        self.message_dir.set(fd.askopenfilename())

    def execute(self):
        print('Insertion Started!')
        print('> video dir:', self.video_dir.get())
        print('> Message dir:', self.message_dir.get())
        print('> Key:', self.key_entry.get())
        print('> Random:', self.random_frame.get())
        print('> Encrypt:', self.output_name.get())

        file_dir = self.video_dir.get()
        message_dir = self.message_dir.get()
        key = self.key_entry.get()
        output_filename = self.output_name.get()

        if file_dir == '' or message_dir == '' or key == '' or output_filename == '':
            return
        
        is_encrypt = self.encrypt.get()
        is_random_frame = self.random_frame.get()
        is_random_pixel = self.random_pixel.get()

        try:
            insert = Inserter(file_dir, message_dir, key)
            original_frames = insert.ori_frames
            inserted_frames = insert.insert_message(
                is_encrypt,
                is_random_frame,
                is_random_pixel
            )
            changes_frame_index = insert.changes_frame_index
            output_file_dir = f"output/video/{output_filename}.avi"
            save_images_to_video(
                output_file_dir,
                insert.directory_img,
                inserted_frames,
                insert.frame_rate,
                insert.is_have_audio,
                insert.directory_audio,
                insert.directory_video
            )
            psnr_value = count_psnr_video(
                original_frames,
                inserted_frames,
                changes_frame_index
            )

            title = 'Finish Insert Secret Message to Video'
            self.controller.show_end_frame(
                title, 
                'Video', 
                output_file_dir, 
                psnr_value
            )
        except:
            print('Error when insert secret message!')
