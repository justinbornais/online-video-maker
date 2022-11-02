from moviepy.editor import *
import os

if __name__ == '__main__':
    
    clip = VideoFileClip('videos/sample.mp4').rotate(180)
    clip.write_videofile('sup.mp4', threads=16, codec="h264_nvenc")
    print("Epic.")