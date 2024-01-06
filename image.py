from PIL import Image, ImageDraw, ImageFont
import requests
from fruit import Fruit
from io import BytesIO
import logging

size = 500, 160

def create_fruit_image(fruit: Fruit):

    logging.info(f"[IMG] Creating image for fruit {fruit.name}...")

    logging.info("[IMG] Getting fruit image...")
    resp = requests.get(url=fruit.image_url)

    logging.info("[IMG] Fruit image got!")

    fruit_image = Image.open(BytesIO(resp.content))

    image = Image.new(mode="RGBA", size=size, color=fruit.background_color)

    draw = ImageDraw.Draw(image)

    logging.info("[IMG] Drawing rectanagles...")
    draw.rounded_rectangle([(15, 15), (size[0] - 15, size[-1] - 15)], fill=fruit.foreground_color, radius=5)
    draw.rounded_rectangle([(30, 30), (130, 130)], fill=fruit.fruit_image_color, radius=5)
    logging.info("[IMG] Drawed!")

    logging.info("[IMG] Importing fonts...")
    bold_font = ImageFont.truetype("fonts/bold.ttf", 35)
    regular_font = ImageFont.truetype("fonts/regular.ttf", size=32)
    logging.info("[IMG] Imported all fonst!")

    draw.text([160, 30], text=fruit.name.upper(), font=bold_font, fill=fruit.text_color)
    draw.text([160, 80], text=f"$ {fruit.price}", font=regular_font, fill=fruit.fruit_image_color)

    logging.info("[IMG] Pasting fruit image...")
    image.paste(fruit_image, (30, 30), fruit_image)
    logging.info("[IMG] Fruit image pasted in main image!")

    logging.info("[IMG] Successfully created image for fruit!")

    return image