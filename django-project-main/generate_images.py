from PIL import Image, ImageDraw, ImageFont
import os

# Create static/img directory if it doesn't exist
os.makedirs('static/img', exist_ok=True)

# Generate about hero image
img = Image.new('RGB', (800, 600), color=(73, 109, 137))
d = ImageDraw.Draw(img)
d.text((400, 300), 'About Us', fill=(255, 255, 255), anchor='mm')
img.save('static/img/about-hero.jpg')

# Generate team member images
for i in range(1, 4):
    img = Image.new('RGB', (400, 400), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((200, 200), f'Team Member {i}', fill=(255, 255, 255), anchor='mm')
    img.save(f'static/img/team-{i}.jpg') 