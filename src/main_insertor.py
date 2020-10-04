from audio.insertor import Inserter
from helper.file import File


file_dir = 'sample/audio/StarWars3.wav'
secret_message_dir = 'sample/text/message.txt'
key = "kuncirahasia"

insert = Inserter(file_dir, secret_message_dir, key)

frame_modified = insert.insert_message(
    randomize_bytes=False,
    randomize_frames=False,
    encrypted=False,
)

output_filename = 'output/output.wav'
output_file = File(output_filename)
output_file.write_audio_file(frame_modified, insert.params)