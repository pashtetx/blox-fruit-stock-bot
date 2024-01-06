from PIL import Image, ImageDraw, ImageFont
import requests
from fruit import Fruit
from io import BytesIO

size = 500, 160

def create_fruit_image(fruit: Fruit):

    resp = requests.get(url=fruit.image_url)

    fruit_image = Image.open(BytesIO(resp.content))

    image = Image.new(mode="RGBA", size=size, color=fruit.background_color)

    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle([(15, 15), (size[0] - 15, size[-1] - 15)], fill=fruit.foreground_color, radius=5)
    draw.rounded_rectangle([(30, 30), (130, 130)], fill=fruit.fruit_image_color, radius=5)

    bold_font = ImageFont.truetype("fonts/bold.ttf", 35)
    regular_font = ImageFont.truetype("fonts/regular.ttf", size=32)

    draw.text([160, 30], text=fruit.name.upper(), font=bold_font, fill=fruit.text_color)
    draw.text([160, 80], text=f"$ {fruit.price}", font=regular_font, fill=fruit.fruit_image_color)

    image.paste(fruit_image, (30, 30), fruit_image)

    return image