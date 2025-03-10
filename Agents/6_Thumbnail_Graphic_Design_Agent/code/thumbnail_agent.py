#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

def create_thumbnail():
    # Create a simple image with a solid background (black)
    img = Image.new('RGB', (1280, 720), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Define the text for the thumbnail
    text = "Thumbnail for Breaking News on Asap Rocky"
    text_color = (255, 255, 255)
    
    # Load the default font
    font = ImageFont.load_default()
    
    # Calculate text size using the default font's getbbox() method
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate the position to center the text
    position = ((1280 - text_width) / 2, (720 - text_height) / 2)
    
    # Draw the text on the image using the default font
    d.text(position, text, fill=text_color, font=font)
    
    # Save the image
    output_file = os.path.join(
        os.path.expanduser("~"),
        "Documents/youtube/Agents/6_Thumbnail_Graphic_Design_Agent/code/thumbnail.jpg"
    )
    img.save(output_file)
    print("Thumbnail created and saved to", output_file)

if __name__ == '__main__':
    create_thumbnail()
