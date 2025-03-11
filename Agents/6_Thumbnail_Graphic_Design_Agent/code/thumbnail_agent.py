"""
Thumbnail Design Agent

Purpose: Creates YouTube thumbnails from text templates
Input: Title text, style preferences
Output: Thumbnail image file
Dependencies: Pillow (PIL)
"""

from PIL import Image, ImageDraw, ImageFont
import os

def generate_thumbnail(title: str, output_path: str = "thumbnail.png") -> str:
    """Generates YouTube thumbnail with specified text.
    
    Args:
        title: Video title text
        output_path: Output file path
        
    Returns:
        Path to generated thumbnail
        
    Raises:
        OSError: If font file is missing
    """
    # Create blank image
    img = Image.new("RGB", (1280, 720), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("fonts/arial-bold.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
        
    # Center text
    text_width, text_height = draw.textsize(title, font=font)
    x = (1280 - text_width) / 2
    y = (720 - text_height) / 2
    
    # Add text
    draw.text((x, y), title, fill=(255, 255, 255), font=font)
    
    # Save output
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    result = generate_thumbnail("AI Revolution in 2024")
    print(f"Thumbnail saved to: {result}")
