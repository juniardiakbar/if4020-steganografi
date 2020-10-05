from tkinter import messagebox
import numpy as np

import random
import base64

from src.helper.file import File
from src.helper.cipher import encrypt_vigenere

Wc = np.indices((8, 8)).sum(axis=0) % 2


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

    def random_list(self, randomize_frames):
        sign = 1 if randomize_frames else 0

        self.ndarray[0][0][1] = self.ndarray[0][0][1] & 254 | sign
        if randomize_frames:
            random.seed(self.seed)
            if self.method == 'lsb':
                random.shuffle(self.pixel_list)
            elif self.method == 'bpcs':
                random.shuffle(self.block_list)

    def modify_pixel(self, array_bit):
        index = 0
        for i in self.pixel_list:
            if index >= len(array_bit):
                break
            if i >= 3:
                h, w, color = self.get_ndarray_pos(i)
                self.ndarray[h][w][color] = self.ndarray[h][w][color] & 254 | array_bit[index]
                index += 1
        if index < len(array_bit):
            error = "Ukuran pesan melebihi kapasitas payload!"
            messagebox.showerror("Kesalahan", error)
            raise RuntimeError(error)

    def insert_alpha(self):
        alpha_str = str(self.alpha)[:7].ljust(7, '0')
        alpha_bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in alpha_str])))
        index = 0
        for i in range(1, 8):
            for j in range(8):
                self.ndarray[i][j][0] = self.ndarray[i][j][0] & 254 | alpha_bits[index]
                index += 1

    def pbc_to_cgc(self):
        b = self.ndarray
        g = b >> 7
        for i in range(7, 0, -1):
            g <<= 1
            g |= ((b >> i) & 1) ^ ((b >> (i - 1)) & 1)
        self.ndarray = g

    def cgc_to_pbc(self):
        g = self.ndarray
        b = g >> 7
        for i in range(7, 0, -1):
            b_before = b.copy()
            b <<= 1
            b |= (b_before & 1) ^ ((g >> (i - 1)) & 1)
        self.ndarray = b

    def complexity(self, matrix):
        maxim = ((matrix.shape[0] - 1) * matrix.shape[1]) + ((matrix.shape[1] - 1) * matrix.shape[0])
        curr = 0.0
        first = matrix[0,0]
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if (first != matrix[i,j]):
                    curr = curr + 1
                    first = matrix[i,j]
        first = matrix[0,0]
        for i in range(matrix.shape[1]):
            for j in range(matrix.shape[0]):
                if (first != matrix[j,i]):
                    curr = curr + 1
                    first = matrix[j,i]
        return curr/maxim
    
    def conjugate(self, P):
        return P ^ Wc

    def modify_block(self, array_bit):
        index = 0
        for bitplane in range(7, -1, -1):
            # bitplane 0 = msb, 7 = lsb
            for h, w, color in self.block_list:
                if index >= len(array_bit):
                    break
                if h != 0 and w != 0 and color != 0:
                    matrix = self.ndarray[h:h+8, w:w+8, color] >> (7 - bitplane) & 1
                    if self.complexity(matrix) > self.alpha:
                        current_bit = np.zeros((8, 8), dtype=int)
                        for i in range(8):
                            for j in range(8):
                                if (i > 0 or j > 0) and index < len(array_bit):
                                    current_bit[i, j] = array_bit[index]
                                    index += 1

                        if self.complexity(current_bit) <= self.alpha:
                            current_bit = self.conjugate(current_bit)
                            current_bit[0, 0] = 1

                        left = (self.ndarray[h:h+8, w:w+8, color] >> (8 - bitplane)) << (8 - bitplane)
                        right = self.ndarray[h:h+8, w:w+8, color] & ((1 << (8 - bitplane - 1)) - 1)
                        self.ndarray[h:h+8, w:w+8, color] = left + (current_bit << 7 - bitplane) + right
            if index >= len(array_bit):
                break
        if index < len(array_bit):
            error = "Ukuran pesan melebihi kapasitas payload!"
            messagebox.showerror("Kesalahan", error)
            raise RuntimeError(error)

    def get_ndarray_pos(self, idx):
        color = idx % self.color
        w = (idx // self.color) % self.w
        h = idx // (self.color * self.w)
        return h, w, color

    def insert_message(self, encrypted=False, randomize=False, method='bpcs', alpha=0.3):
        self.seed = self.count_seed()
        self.method = method
        self.alpha = alpha

        self.string_message = str(len(self.message)) + '#' + self.extension + '#' + self.message
        self.encrypt_message(encrypted, self.key)

        bits = map(int, ''.join(
            [bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.string_message]))
        array_bit = list(bits)

        if method == 'lsb':
            self.pixel_list = list(range(self.h * self.w * self.color))
            self.random_list(randomize)
            self.modify_pixel(array_bit)
            self.ndarray[0, 0, 2] = self.ndarray[0, 0, 2] & 254
        elif method == 'bpcs':
            self.block_list = []
            for h in range(0, self.h - (self.h % 8), 8):
                for w in range(0, self.w - (self.w % 8), 8):
                    for color in range(0, self.color):
                        self.block_list += [(h, w, color)]
            self.random_list(randomize)
            self.pbc_to_cgc()
            self.modify_block(array_bit)
            self.cgc_to_pbc()
            self.insert_alpha()
            self.ndarray[0, 0, 2] = self.ndarray[0, 0, 2] & 254 | 1

        return self.ndarray
