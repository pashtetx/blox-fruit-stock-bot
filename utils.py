from typing import List
from fruit import Fruit
import logging

def get_rarity(fruits):

    rarities = []

    for fruit in fruits:
        span = fruit.find("span")
        if not span:
            continue
        class_ = "".join(span["class"])
        if "Mythical" in class_:
            rarities.append("Mythical")
        elif "Legendary" in class_:
            rarities.append("Legendary")
        elif "Rare" in class_:
            rarities.append("Rare")
        elif "Uncommon" in class_:
            rarities.append("Uncommon")
        elif "Common" in class_:
            rarities.append("Common")
        # rarities.append()
    return rarities


def fruit_converter(stock_html: str) -> List[Fruit]:
    logging.info("[Fruit converter] starting...")

    logging.info("[Fruit converter] Getting fruit images...")
    images = stock_html.find_all("img", class_="thumbimage")
    image_urls = list(dict.fromkeys([img['src'] for img in images if img['src'].startswith("https://")]))
    image_urls.reverse()
    logging.info(f"[Fruit converter] Got fruit images! image={image_urls}")

    logging.info("[Fruit converter] Getting fruit data...")
    fruits_html = stock_html.find_all("b")
    fruits_data = list(dict.fromkeys([i.text for i in fruits_html if not i.find("img", class_="thumbimage")]))

    fruits_data.reverse()

    logging.info("[Fruit converter] Got fruit data!")

    logging.info("[Fruit converter] Getting fruit prices...")
    prices = list(filter(lambda fruit: fruit.replace(",", "").replace(" ", "").isdigit(),fruits_data))
    logging.info(f"[Fruit converter] Got fruit prices! prices={prices}")

    logging.info(f"[Fruit converter] Getting fruit names...")
    names = list(filter(lambda fruit: not fruit.replace(",", "").replace(" ", "").isdigit(),fruits_data))
    logging.info(f"[Fruit converter] Got fruit names! names={names}")

    logging.info("[Fruit converter] Getting fruits rarities...")
    fruits = list(dict.fromkeys(filter(lambda fruit: not fruit.text.replace(",", "").replace(" ", "").isdigit(), fruits_html)))
    fruits.reverse()

    rarity = get_rarity(fruits)
    logging.info(f"[Fruit converter] Got fruits rarities! rarities={rarity}")

    fruits = []

    for i in range(len(names)):
        fruits.append(Fruit(name=names[i], rarity=rarity[i], price=prices[i], image_url=image_urls[i]))
    
    logging.info(f"[Fruit converter] Fruits converter successfully ended! fruits={fruits}")

    return fruits