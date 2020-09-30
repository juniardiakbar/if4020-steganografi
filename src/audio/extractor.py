import wave
import random
import base64

from helper.file import File
from vigenere.cipher import decrypt_vigenere


class Extractor:
    def __init__(self, file_dir, key):
        stegano_audio_file = File(file_dir)
        self.frame = stegano_audio_file.read_frame_audio_file()

        self.key = key

    def count_seed(self):
        return sum([ord(i) for i in self.key])

    def extract_messages(self):
        # Get sign from LSB
        encrypted = bin(self.frame[0])[-1] == '1'
        random_frames = bin(self.frame[1])[-1] == '1'
        opt = 2 if bin(self.frame[2])[-1] == '1' else 1

        self.seed = self.count_seed()

        index = 0
        temp = ""
        message = ""

        # Extract the LSB of each byte
        if opt == 1:
            mod_index = 8
            extracted = [self.frame[i] & 1 for i in range(len(self.frame))]

        # Extract the 2 LSB of each byte
        elif opt == 2:
            mod_index = 4
            extracted = [bin(self.frame[i] & 3).lstrip('0b').rjust(
                2, '0') for i in range(len(self.frame))]

        # Handling random frame case
        frame_list = list(range(len(extracted)))
        if random_frames:
            random.seed(self.seed)
            random.shuffle(frame_list)

        # Get all in string format
        for i in frame_list:
            if i >= 3:
                if index % mod_index != (mod_index - 1):
                    temp += str(extracted[i])
                else:
                    temp += str(extracted[i])
                    message += chr(int(temp, 2))
                    temp = ""

                index += 1

        # Decrypt if needed
        if encrypted:
            self.string_message = decrypt_vigenere(message, self.key)
        else:
            self.string_message = message

    # Get the sign of message in audio (length, extension)
    def parse_message(self):
        message_info = self.string_message.split("#")

        self.len_message = int(message_info[0])
        self.extension = message_info[1]

    def write_secret_message(self):
        init = len(str(self.len_message)) + \
            len(str(self.extension)) + 2  # Get init index
        decoded = self.string_message[init:init + self.len_message]

        # Convert to bytes
        bytes_file = decoded.encode('utf-8')
        bytes_file = base64.b64decode(bytes_file)

        return bytes_file
