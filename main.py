from moviepy.editor import *
from PIL import Image
from PIL import ImageDraw, ImageFont
import PIL
import numpy as np
import os

FONT = 'open-sans/OpenSans-Regular.ttf'

if __name__ == '__main__':
    
    # Get all the image files.
    file_list = [n for n in os.listdir('images/') if (n.endswith('.jpg') or n.endswith('.png'))]
    
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
        
        
        # Display edited image
        #img.show()
        
        # Save the edited image
        end = ''
        if '.png' in image: end = '.png'
        elif '.jpg' in image:
            end = '.jpg'
            img = img.convert('RGB')
        
        img.save("processed_images/" + image)
        print(image)
    clip = VideoFileClip('videos/sample.mp4').rotate(180)
    
    img = Image.open('processed_images/block.png')
    img = np.array(img)
    img = ImageClip('processed_images/block.png')
    clip = concatenate([clip, img.set_start(clip.duration).set_duration(5)], method='compose')
    clip.write_videofile('sup.mp4', threads=16, codec="h264_nvenc", verbose=False, logger=None)
    print("Epic.")