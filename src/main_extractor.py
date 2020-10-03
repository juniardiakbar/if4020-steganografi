from audio.extractor import Extractor
from helper.file import File


file_dir = 'output/output.wav'
key = "kuncirahasia"

extract = Extractor(file_dir, key)
extract.extract_messages()
extract.parse_message()

output_filename = 'output/output.txt'
output_file = File(output_filename)
byte = extract.get_secret_message()
output_file.write_files(byte)
