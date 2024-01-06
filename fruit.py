from enum import Enum


colors = {
    "Common": {
        "background": (230, 230, 230, 0),
        "foreground":(90, 90, 90),
        "fruit-image-background":(60, 60, 60),
        "fruit-text":(240, 240, 240),
    }
    ,"Uncommon": {
        "background": (230, 230, 230, 0),
        "foreground":(71, 108, 163),
        "fruit-image-background":(62, 62, 255),
        "fruit-text":(59, 60, 179),
    },
    "Rare": {
        "background": (230, 230, 230, 0),
        "foreground":(30, 0, 52),
        "fruit-image-background":(78, 0, 108),  
        "fruit-text":(78, 0, 134),
    },
    "Legendary": {
        "background": (230, 230, 230, 0),
        "foreground":(94, 2, 65),
        "fruit-image-background":(57, 2, 44),
        "fruit-text":(148, 2, 122),
    },
    "Mythical": {
        "background": (230, 230, 230, 0),
        "foreground":(242, 48, 51),
        "fruit-image-background":(164, 48, 51),
        "fruit-text":(150, 44, 39),
    }
}



class Fruit:

    def __init__(self, rarity: str, name: str, price: int, image_url: str) -> None:
        self.rarity = rarity

        self.name = name
        self.price = price
        self.image_url = image_url
    
    @property
    def background_color(self):
        return colors[self.rarity].get("background")
    
    @property
    def foreground_color(self):
        return colors[self.rarity].get("foreground")

    @property
    def fruit_image_color(self):
        return colors[self.rarity].get("fruit-image-background")
    
    @property
    def text_color(self):
        return colors[self.rarity].get("fruit-text")

    def __str__(self) -> str:
        return f"<{self.name}, {self.rarity}>"

    def __repr__(self) -> str:
        return f"<{self.name}, {self.rarity}>"