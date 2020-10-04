from tkinter import messagebox

import random
import base64

from src.helper.file import File
from src.helper.cipher import encrypt_vigenere


class Inserter:
    def __init__(self, file_dir, secret_message_dir, key):
        image_file = File(file_dir)
        self.ndarray = image_file.read_ndarray_image_file()
        self.h, self.w, self.color = self.ndarray.shape

        secret_message = File(secret_message_dir)
        self.extension = secret_message.get_extention()
        self.string_message = ""

        byte_message = secret_message.read_files()
        self.message = base64.b64encode(byte_message).decode('utf-8')

        self.key = key

    def count_seed(self):
        return sum([ord(i) for i in self.key])

    def encrypt_message(self, encrypted, key):
        sign = 1 if encrypted else 0

        self.ndarray[0][0][0] = self.ndarray[0][0][0] & 254 | sign
        if encrypted:
            self.string_message = encrypt_vigenere(self.string_message, key)

    def random_pixel(self, randomize_frames):
        sign = 1 if randomize_frames else 0

        self.ndarray[0][0][1] = self.ndarray[0][0][1] & 254 | sign
        if randomize_frames:
            random.seed(self.seed)
            random.shuffle(self.pixel_list)

    def modify_pixel(self, array_bit):
        index = 0
        for i in self.pixel_list:
            if index >= len(array_bit):
                break
            if i >= 2:
                h, w, color = self.get_ndarray_pos(i)
                self.ndarray[h][w][color] = self.ndarray[h][w][color] & 254 | array_bit[index]
                index += 1
        if index < len(array_bit):
            error = "Ukuran pesan melebihi kapasitas payload!"
            messagebox.showerror("Kesalahan", error)
            raise RuntimeError(error)

    def get_ndarray_pos(self, idx):
        color = idx % self.color
        w = (idx // self.color) % self.w
        h = idx // (self.color * self.w)
        return h, w, color

    def insert_message(self, encrypted=False, randomize=False):
        self.seed = self.count_seed()

        self.string_message = str(len(self.message)) + '#' + self.extension + '#' + self.message
        self.encrypt_message(encrypted, self.key)

        bits = map(int, ''.join(
            [bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.string_message]))
        array_bit = list(bits)

        self.pixel_list = list(range(self.h * self.w * self.color))
        self.random_pixel(randomize)
        self.modify_pixel(array_bit)

        return self.ndarray
