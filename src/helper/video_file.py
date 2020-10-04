import ffmpeg
import numpy as np
import subprocess, uuid, os, shutil
from PIL import Image
from math import log10, sqrt


class VideoFile:
    def __init__(self, filename):
        self.filename = filename
        self.directory_img = '../tmp/' + str(uuid.uuid4())
        self.frame_rate = self.get_frame_rate()
        self.resolution = self.get_resolution()
        self.frames = self.read_frames()
    
    def get_frame_rate(self):
        command = [ 
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=r_frame_rate',
            '-of', 'csv=s=x:p=0',
            self.filename
        ]
        cmd_out, cmd_error = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
        string = str(cmd_out)
        tmp = string[2:string.find('\\')]
        frame_speed, divisor = tmp.split('/')
        frame_rate = int(frame_speed) / int(divisor)

        return frame_rate
    
    def get_resolution(self):
        command = [ 
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0',
            self.filename
        ]

        cmd_out, cmd_error = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
        string = str(cmd_out)
        tmp = string[2:string.find('\\')]
        width, height = tmp.split('x')

        return (int(width), int(height))
    
    def read_frames(self):
        input_video, _ = (
            ffmpeg
            .input(self.filename)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True)
        )
        
        width, height = self.resolution

        frames = (
            np
            .frombuffer(input_video, np.uint8)
            .reshape([-1, int(height), int(width), 3])
        )

        return frames
    
def save_frames_to_image(directory_img, frames):
    os.makedirs(directory_img)
    count = 0
    for frame in frames:
        image = Image.fromarray(frame)
        image.save(directory_img + '/frame%d.png' % count)
        count += 1

def save_images_to_video(output_path, directory_img, frames, frame_rate):
    save_frames_to_image(directory_img, frames)

    command = [ 
        'ffmpeg',
        '-r', str(frame_rate),
        '-i', directory_img + '/frame%d.png',
        '-vcodec', 'ffv1',
        '-y',
        output_path 
    ]
    retcode = subprocess.call(command)

    shutil.rmtree('../tmp/')

def psnr_frame(ori_frame, modified_frame):
    mse = np.mean((ori_frame - modified_frame) ** 2)
    if (mse == 0):
        return 100
    max_pixel = 255
    psnr = 20 * log10(max_pixel / sqrt(mse))

    return psnr

def count_psnr_video(ori, modified, changes_index):
    number_of_changes = len(changes_index)
    psnr = 0
    for i in range(number_of_changes):
        idx = changes_index[i]
        psnr += psnr_frame(ori[idx], modified[idx])
    
    return 100 if (number_of_changes == 0) else psnr / number_of_changes