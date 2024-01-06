from typing import List
from fruit import Fruit

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
    images = stock_html.find_all("img", class_="thumbimage")
    image_urls = list(dict.fromkeys([img['src'] for img in images if img['src'].startswith("https://")]))
    image_urls.reverse()

    fruits_html = stock_html.find_all("b")
    fruits_data = list(dict.fromkeys([i.text for i in fruits_html if not i.find("img", class_="thumbimage")]))

    fruits_data.reverse()

    prices = list(filter(lambda fruit: fruit.replace(",", "").replace(" ", "").isdigit(),fruits_data))
    
    names = list(filter(lambda fruit: not fruit.replace(",", "").replace(" ", "").isdigit(),fruits_data))
    
    fruits = list(dict.fromkeys(filter(lambda fruit: not fruit.text.replace(",", "").replace(" ", "").isdigit(), fruits_html)))
    fruits.reverse()

    rarity = get_rarity(fruits)

    fruits = []

    for i in range(len(names)):
        fruits.append(Fruit(name=names[i], rarity=rarity[i], price=prices[i], image_url=image_urls[i]))
    
    return fruits