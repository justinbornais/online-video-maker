from moviepy.editor import *
from PIL import Image
from PIL import ImageDraw
import os

if __name__ == '__main__':
    
    clip = VideoFileClip('videos/sample.mp4').rotate(180)
    clip.write_videofile('sup.mp4', threads=16, codec="h264", verbose=False, logger=None)
    print("Epic.")