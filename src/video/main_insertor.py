from src.video.insertor import Inserter
from src.helper.video_file import *

if (__name__== "__main__" ):
    path = 'sample/video/ex1.avi'
    message_path = 'sample/text/short.txt'
    key = 'irfan'

    insert = Inserter(path, message_path, key)
    inserted_frames = insert.insert_message(
        is_encrypt = False,
        is_random_frame = False,
        is_random_pixel = False
    )

    output_path = 'sample/video/inserted.avi'
    save_images_to_video(
        output_path,
        insert.directory_img,
        inserted_frames,
        insert.frame_rate
    )

    tes_vid = VideoFile(output_path)
    tes_frames = tes_vid.frames

    input_vid = VideoFile(path)
    input_frames = input_vid.frames

    print((inserted_frames == tes_frames).all())
    print((input_frames == tes_frames).all())