import random, base64, copy
import numpy as np

from src.helper.file import File
from src.helper.video_file import *
from src.helper.cipher import decrypt_vigenere

class Extractor:
    def __init__(self, file_dir, key):
        # Extract video
        video_file = VideoFile(file_dir)
        self.frames = copy.deepcopy(video_file.frames)
        self.frame_rate = video_file.frame_rate
        self.resolution = video_file.resolution
        self.number_of_frames = len(self.frames)
        
        self.key = key
        self.frame_list = list(range(self.number_of_frames))
        self.height_list = list(range(self.resolution[1]))
        self.width_list = list(range(self.resolution[0]))
    
    def count_seed(self):
        return sum([ord(i) for i in self.key])
    
    def extract_message(self):
        self.seed = self.count_seed()

        # GET information about LSB algorithm
        is_encrypt = self.frames[0][0][0][0] & 1
        is_random_frame = self.frames[0][0][0][1] & 1
        is_random_pixel = self.frames[0][0][0][2] & 1

        # Shuffle frame_list if needed
        if (is_random_frame):
            random.seed(self.seed)
            random.shuffle(self.frame_list)
        
        # Shuffle pixel if needed
        if (is_random_pixel):
            random.seed(self.seed)
            random.shuffle(self.height_list)
            random.shuffle(self.width_list)
        
        tmp = ''
        message = ''
        index = 0
        cnt_border = 0
        len_message = 0
        cnt_message = 0
        flag_found = False
    
        for idx_frame in self.frame_list:
            for idx_height in self.height_list:
                for idx_width in self.width_list:
                    if (idx_frame == 0 and idx_height == 0 and idx_width == 0):
                        continue
                    else:
                        rgb_bytes = self.frames[idx_frame][idx_height][idx_width]
                        for byte in rgb_bytes:
                            lsb = byte & 1
                            if (index % 8 != 7):
                                tmp += str(lsb)
                            else:
                                tmp += str(lsb)
                                char = chr(int(tmp, 2))
                                message += char
                                if (flag_found):
                                    cnt_message += 1
                                    if (cnt_message == len_message):
                                        break
                                if (is_encrypt):
                                    char = decrypt_vigenere(char, self.key)
                                if (char == '#'):
                                    cnt_border += 1
                                if (cnt_border == 2):
                                    tmp_message = message
                                    if (is_encrypt):
                                        tmp_message = decrypt_vigenere(tmp_message, self.key)
                                    info = tmp_message.split('#')
                                    flag_found = True
                                    len_message = int(info[0])
                                tmp = ''
                            index += 1
                        if (cnt_message == len_message and flag_found):
                            break
                if (cnt_message == len_message and flag_found):
                    break 
            if (cnt_message == len_message and flag_found):
                break        
                  
        if (is_encrypt):
            self.string_message = decrypt_vigenere(message, self.key)
        else:
            self.string_message = message
    
    def parse_message(self):
        message_info = self.string_message.split('#')

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