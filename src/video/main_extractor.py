from src.video.extractor import Extractor
from src.helper.video_file import *
from src.helper.file import File

if (__name__=="__main__"):
    file_dir = 'sample/video/inserted.avi'
    key = 'irfan'

    extract = Extractor(file_dir, key)
    extract.extract_message()
    extract.parse_message()

    output_filename = 'sample/text/vid_output.txt'
    output_file = File(output_filename)
    byte = extract.write_secret_message()
    output_file.write_files(byte)