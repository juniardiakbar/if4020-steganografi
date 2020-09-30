import wave
import random
import base64

from helper.file import File
from vigenere.cipher import encrypt_vigenere


class Inserter:
    def __init__(self, file_dir, secret_message_dir, key):
        audio_file = File(file_dir)
        self.frame = audio_file.read_frame_audio_file()
        self.params = audio_file.get_params_audio()

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

        self.frame[0] = self.frame[0] & 254 | sign
        if encrypted:
            self.string_message = encrypt_vigenere(self.string_message, key)

    def random_frame(self, randomize_frames):
        sign = 1 if randomize_frames else 0

        self.frame[1] = self.frame[1] & 254 | sign
        if randomize_frames:
            random.seed(self.seed)
            random.shuffle(self.frame_list)

    def modify_frame(self, array_bit):
        index = 0
        self.frame[2] = self.frame[2] & 254 | 0
        for i in self.frame_list:
            if index >= len(array_bit):
                break
            if i >= 3:
                self.frame[i] = self.frame[i] & 254 | array_bit[index]
                index += 1

    def insert_message(self, encrypted=False, randomize_bytes=False, randomize_frames=False):
        self.seed = self.count_seed()

        len_message = str(len(self.message))
        self.string_message = len_message + '#' + self.extension + '#' + self.message
        self.encrypt_message(encrypted, self.key)

        bits = map(int, ''.join(
            [bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.string_message]))
        array_bit = list(bits)

        self.frame_list = list(range(len(self.frame)))
        self.random_frame(randomize_frames)
        self.modify_frame(array_bit)

        return bytes(self.frame)
