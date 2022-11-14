from math import ceil, floor
from moviepy.editor import *
from PIL import Image
from PIL import ImageDraw, ImageFont
import PIL
import numpy as np
import os

FONT = 'open-sans/OpenSans-Regular.ttf'
WIDTH = 1280
HEIGHT = 720

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
    
    first_length = 0
    second_length = 0
    
    length_per_clip = 0
    if first_length != 0 and second_length != 0: length_per_clip = total_length / (len(file_list) - 2)
    elif first_length != 0 or second_length != 0: length_per_clip = total_length / (len(file_list) - 1)
    else: length_per_clip = total_length / len(file_list)
    
    print(f"{total_length} - {length_per_clip}")
    
    
    for image in file_list:
        
        # Open an Image and immediately scale it to the proper resolution.
        img = Image.open('images/' + image)
        multiplier = min(WIDTH/img.width, HEIGHT/img.height)
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
        
        if img.width < WIDTH:
            img = add_margin(img, 0, ceil((WIDTH - img.width) / 2), 0, floor((WIDTH - img.width) / 2), (0, 0, 0))
        elif img.height < HEIGHT:
            img = add_margin(img, ceil((HEIGHT - img.height) / 2), 0, floor((HEIGHT - img.height) / 2), 0, (0, 0, 0))
        
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
    
    clip = None
    for i in imgs:
        if clip == None:
            clip = concatenate([i.set_start(0).set_duration(length_per_clip)], method='compose')
            continue
        clip = concatenate([clip, i.set_start(clip.duration).set_duration(length_per_clip)], method='compose')
    
    clip.fps = 24
    clip.write_videofile('sup2.mp4',  threads=16, codec="h264_nvenc", verbose=False)#, logger=None)
    print(f'Video created: Size = {clip.size}')