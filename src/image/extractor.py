import random
import base64

from src.helper.file import File
from src.helper.cipher import decrypt_vigenere


class Extractor:
    def __init__(self, file_dir, key):
        stegano_image_file = File(file_dir)
        self.ndarray = stegano_image_file.read_ndarray_image_file()
        self.h, self.w, self.color = self.ndarray.shape
        self.key = key

    def count_seed(self):
        return sum([ord(i) for i in self.key])

    def get_ndarray_pos(self, idx):
        color = idx % self.color
        w = (idx // self.color) % self.w
        h = idx // (self.color * self.w)
        return h, w, color

    def extract_messages(self):
        self.seed = self.count_seed()
        
        extracted = [self.ndarray[self.get_ndarray_pos(i)] & 1 for i in range(self.h * self.w * self.color)]
        encrypted = extracted[0]
        random_pixels = extracted[1]

        index = 0
        mod_index = 8

        message = ""
        temp = ""

        pixel_list = list(range(len(extracted)))
        if random_pixels:
            random.seed(self.seed)
            random.shuffle(pixel_list)

        for i in pixel_list:
            if i >= 2:
                if index % mod_index != (mod_index - 1):
                    temp += str(extracted[i])
                else:
                    temp += str(extracted[i])
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
