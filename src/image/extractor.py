import numpy as np

import random
import base64

from src.helper.file import File
from src.helper.cipher import decrypt_vigenere

Wc = np.indices((8, 8)).sum(axis=0) % 2


class Extractor:
    def __init__(self, file_dir, key):
        stegano_image_file = File(file_dir)
        self.ndarray = stegano_image_file.read_ndarray_image_file()
        self.h, self.w, self.color = self.ndarray.shape
        self.key = key

    def conjugate(self, P):
        return P ^ Wc

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

    def count_seed(self):
        return sum([ord(i) for i in self.key])

    def get_ndarray_pos(self, idx):
        color = idx % self.color
        w = (idx // self.color) % self.w
        h = idx // (self.color * self.w)
        return h, w, color

    def extract_alpha(self):
        index = 0
        mod_index = 8
        temp = ""
        alpha_str = ""

        for i in range(1, 8):
            for j in range(8):
                extracted = self.ndarray[i][j][0] & 1
                if index % mod_index != (mod_index - 1):
                    temp += str(extracted)
                else:
                    temp += str(extracted)
                    alpha_str += chr(int(temp, 2))
                    temp = ""
                index += 1
        return float(alpha_str)

    def extract_messages(self):
        self.seed = self.count_seed()

        extracted = [self.ndarray[self.get_ndarray_pos(i)] & 1 for i in range(self.h * self.w * self.color)]
        encrypted = extracted[0]
        random_pixels = extracted[1]
        method = 'bpcs' if extracted[2] else 'lsb'

        index = 0
        mod_index = 8

        message = ""
        temp = ""

        if method == 'lsb':
            pixel_list = list(range(len(extracted)))
            if random_pixels:
                random.seed(self.seed)
                random.shuffle(pixel_list)

            for i in pixel_list:
                if i >= 3:
                    if index % mod_index != (mod_index - 1):
                        temp += str(extracted[i])
                    else:
                        temp += str(extracted[i])
                        message += chr(int(temp, 2))
                        temp = ""
                    index += 1
        elif method == 'bpcs':
            alpha = self.extract_alpha()
            block_list = []
            for h in range(0, self.h - (self.h % 8), 8):
                for w in range(0, self.w - (self.w % 8), 8):
                    for color in range(0, self.color):
                        block_list += [(h, w, color)]
            if random_pixels:
                random.seed(self.seed)
                random.shuffle(block_list)
            self.pbc_to_cgc()
            for bitplane in range(7, -1, -1):
                for h, w, color in block_list:
                    if h != 0 and w != 0 and color != 0:
                        matrix = self.ndarray[h:h+8, w:w+8, color] >> (7 - bitplane) & 1
                        if self.complexity(matrix) > alpha:
                            if matrix[0, 0]:
                                matrix = self.conjugate(matrix)
                            for i in range(8):
                                for j in range(8):
                                    if i > 0 or j > 0:
                                        extracted_bit = matrix[i][j]
                                        if index % mod_index != (mod_index - 1):
                                            temp += str(extracted_bit)
                                        else:
                                            temp += str(extracted_bit)
                                            message += chr(int(temp, 2))
                                            temp = ""
                                        index += 1

        if encrypted:
            self.string_message = decrypt_vigenere(message, self.key)
        else:
            self.string_message = message

    def parse_message(self):
        message_info = self.string_message.split("#")

        self.len_message = int(message_info[0])
        self.extension = message_info[1]

    def write_secret_message(self):
        init = len(str(self.len_message)) + len(str(self.extension)) + 2
        decoded = self.string_message[init : init + self.len_message]

        bytes_file = decoded.encode('utf-8')
        bytes_file = base64.b64decode(bytes_file)

        return bytes_file
