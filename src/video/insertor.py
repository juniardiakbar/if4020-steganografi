import random, base64, copy
import numpy as np

from src.helper.file import File
from src.helper.video_file import *
from src.helper.cipher import encrypt_vigenere
from tkinter import messagebox

class Inserter:
    def __init__(self, file_dir, message_dir, key):
        # Extract video
        video_file = VideoFile(file_dir)
        self.frames = copy.deepcopy(video_file.frames)
        self.frame_rate = video_file.frame_rate
        self.resolution = video_file.resolution
        self.number_of_frames = len(self.frames)
        self.directory_img = video_file.directory_img

        self.key = key

        # Extract message
        secret_message = File(message_dir)
        self.extension = secret_message.get_extention()
        self.string_message = ''

        byte_message = secret_message.read_files()
        self.message = base64.b64encode(byte_message).decode('utf-8')
    
    def count_seed(self):
        return sum([ord(i) for i in self.key])
    
    def encrypt_message(self, is_encrypt, key):
        sign = 1 if is_encrypt else 0

        self.frames[0][0][0][0] = self.frames[0][0][0][0] & 254 | sign
        if (is_encrypt):
            self.string_message = encrypt_vigenere(self.string_message, key)
    
    def random_frame(self, is_random_frame):
        sign = 1 if is_random_frame else 0
        
        self.frames[0][0][0][1] = self.frames[0][0][0][1] & 254 | sign
        if (is_random_frame):
            random.seed(self.seed)
            random.shuffle(self.frame_list)

    def random_pixel(self, is_random_pixel):
        sign = 1 if is_random_pixel else 0

        self.frames[0][0][0][2] = self.frames[0][0][0][2] & 254 | sign
        if (is_random_pixel):
            random.seed(self.seed)
            random.shuffle(self.height_list)
            random.shuffle(self.width_list)
    
    def modify_pixel(self, idx_frame, idx_height, idx_width, idx_bit):
        array_bit_length = len(self.array_bit)
        i = 0
        while (i < 3):
            if (idx_bit + i < array_bit_length):
                bit = self.array_bit[idx_bit + i]
                awal = self.frames[idx_frame][idx_height][idx_width][i]
                
                self.frames[idx_frame][idx_height][idx_width][i] = awal & 254 | bit
                akhir = self.frames[idx_frame][idx_height][idx_width][i]
                i += 1
            else:
                break
        
        return idx_bit + i
    
    def modify_frames(self):
        idx_bit = 0
        array_bit_length = len(self.array_bit)

        for idx_frame in self.frame_list:
            for idx_height in self.height_list:
                for idx_width in self.width_list:
                    if (idx_frame == 0 and idx_height == 0 and idx_width == 0):
                        continue
                    elif (idx_bit >= array_bit_length):
                        break
                    else:
                        idx_bit = self.modify_pixel(
                            idx_frame,
                            idx_height,
                            idx_width, 
                            idx_bit
                        )
                if (idx_bit >= array_bit_length):
                    break
            if (idx_bit >= array_bit_length):
                break
        if (idx_bit < array_bit_length):
            error = 'Ukuran pesan melebihi kapasitas payload!'
            messagebox.showerror("Kesalahan", error)
            raise RuntimeError(error)

        return self.frames

    def insert_message(self, is_encrypt = False, is_random_frame = False, is_random_pixel = False):
        self.seed = self.count_seed()
        len_message = str(len(self.message))
        self.string_message = len_message + '#' + self.extension + '#' + self.message
        self.encrypt_message(is_encrypt, self.key)

        bits = map(int, ''.join(
            [bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.string_message]))
        self.array_bit = list(bits)

        self.frame_list = list(range(self.number_of_frames))
        self.height_list = list(range(self.resolution[1]))
        self.width_list = list(range(self.resolution[0]))

        self.random_frame(is_random_frame)
        self.random_pixel(is_random_pixel)

        self.frames = self.modify_frames()
        return self.frames