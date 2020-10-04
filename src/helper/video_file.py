import ffmpeg
import numpy as np
import subprocess, uuid, os, shutil
from PIL import Image


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

        return (width, height)
    
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
    
    def save_frames_to_image(self):
        os.makedirs(self.directory_img)
        count = 0
        for frame in self.frames:
            image = Image.fromarray(frame)
            image.save(self.directory_img + '/frame%d.png' % count)
            count += 1
    
    def save_images_to_video(self, output_path):
        self.save_frames_to_image()

        command = [ 
            'ffmpeg',
            '-r', str(self.frame_rate),
            '-i', self.directory_img + '/frame%d.png',
            '-vcodec', 'ffv1',
            '-y',
            output_path 
        ]
        retcode = subprocess.call(command)

        shutil.rmtree('../tmp/')

# if (__name__=="__main__"):
#     path = '../../sample/video/ex1.avi'
#     inp = VideoFile(path)
#     frames = inp.frames.copy()

#     path_out = '../../sample/video/out.avi'
#     inp.save_images_to_video(path_out)

#     outp = VideoFile(path_out)
#     frames2 = outp.frames.copy()

#     print((frames == frames2).all())
