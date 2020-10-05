from src.video.insertor import Inserter
from src.helper.video_file import *

if (__name__== "__main__" ):
    path = 'sample/video/ex3.avi'
    message_path = 'sample/text/short.txt'
    key = 'irfan'

    insert = Inserter(path, message_path, key)
    inserted_frames = insert.insert_message(
        is_encrypt = False,
        is_random_frame = False,
        is_random_pixel = False
    )