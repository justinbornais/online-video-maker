from math import ceil, floor
from moviepy.editor import *
from PIL import Image
from PIL import ImageDraw, ImageFont
import PIL
import numpy as np
import os

FONT = 'open-sans/OpenSans-Regular.ttf'

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


if __name__ == '__main__':
    
    # Get all the files.
    file_list = [n for n in os.listdir('images/') if (n.endswith('.jpg') or n.endswith('.png'))]
    audio_list = [n for n in os.listdir('audio/') if (n.endswith('.mp3') or n.endswith('.wav'))]
    audios = [AudioFileClip('audio/' + n) for n in audio_list] # Produce audio clips.
    total_length = 0
    for a in audios: total_length += a.duration # Get the total video length from the length of all the audio files.
    
    for image in file_list:
        
        # Open an Image and immediately scale it to 1080p.
        img = Image.open('images/' + image)
        multiplier = min(1920/img.width, 1080/img.height)
        img = img.resize((int(img.width * multiplier), int(img.height * multiplier)), PIL.Image.LANCZOS)
        
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)

        # Custom font style and font size
        fontsize = 1
        myFont = ImageFont.truetype(FONT, fontsize)
        txt = 'sup'
        
        while myFont.getsize(txt)[0] < img.width:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            myFont = ImageFont.truetype(FONT, fontsize)
        
        I1.text((int(img.width * 0.005), int(img.height - myFont.getsize(txt)[1])), txt, fill=(255, 255, 255), font=myFont)
        
        if img.width < 1920:
            img = add_margin(img, 0, ceil((1920 - img.width) / 2), 0, floor((1920 - img.width) / 2), (0, 0, 0))
        elif img.height < 1080:
            img = add_margin(img, ceil((1080 - img.height) / 2), 0, floor((1080 - img.height) / 2), 0, (0, 0, 0))
        
        # Display edited image
        #img.show()
        
        # Save the edited image
        if image.endswith('.jpg'):
            img = img.convert('RGB')
        
        img.save("processed_images/" + image)
        print(f'{image}: {img.width} x {img.height}')
    
    imgs = [ImageClip('processed_images/' + n) for n in file_list]
    #clip = VideoFileClip('videos/sample.mp4').rotate(180).subclip(0, 1)
    
    img = ImageClip('processed_images/block.png')
    #clip = concatenate([clip, img.set_start(clip.duration).set_duration(5)], method='compose')
    clip = concatenate([img.set_start(0).set_duration(5)], method='compose')
    clip.fps = 30
    clip.write_videofile('sup.mp4',  threads=16, codec="h264_nvenc", verbose=False, logger=None)
    print(f'Video created: Size = {clip.size}')