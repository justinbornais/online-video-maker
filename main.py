from moviepy.editor import *
from PIL import Image
from PIL import ImageDraw, ImageFont
import os

FONT = 'open-sans/OpenSans-Regular.ttf'

if __name__ == '__main__':
    
    # Open an Image
    img = Image.open('images/Donald_Trump_official_portrait.jpg')
    
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    # Custom font style and font size
    myFont = ImageFont.truetype(FONT, 400)
    
    # Add Text to an image
    print(f'{img.width} {img.height}')
    I1.text((int(img.width * 0.005), int(img.height * 0.7)), "HBD NICK!", fill=(255, 255, 255), font=myFont)
    
    # Display edited image
    img.show()
    
    # Save the edited image
    img.save("car2.png")
    # clip = VideoFileClip('videos/sample.mp4').rotate(180)
    # clip.write_videofile('sup.mp4', threads=16, codec="h264", verbose=False, logger=None)
    print("Epic.")