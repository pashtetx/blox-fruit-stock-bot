import aiohttp
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
from utils import fruit_converter
from nextcord import Client, File
from image import create_fruit_image
from sqlalchemy.orm import Session
import io
from nextcord.errors import DiscordServerError
from db.channel import get_channels, delete_channel

URL = "https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22"


REFRESH_IN = [2, 6, 10, 14, 18, 22]


def get_next_refresh(hour: int) -> int:
    for next_hour in REFRESH_IN:
        if next_hour > hour:
            return next_hour
    return REFRESH_IN[0] 


async def stock_subscriber(bot: Client, session: Session):
    while True:
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(URL) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                stock = soup.find("div", id="mw-customcollapsible-current")
                fruits = fruit_converter(stock_html=stock)

                for fruit in fruits:

                    arr = io.BytesIO()
                    fruit_image = create_fruit_image(fruit)
                    channels = get_channels(session=session)
                    for channel in channels:
                        fruit_image.save(arr, format="png")
                        arr.seek(0)
                        try:
                            discord_channel = await bot.fetch_channel(channel.channel_id)
                            await discord_channel.send(file=File(
                                arr,
                                filename=f"{fruit.name}.png"
                            ))
                        except DiscordServerError:
                            delete_channel(session=session, channel_id=channel.channel_id)

                now = datetime.now()
                refresh_in = get_next_refresh(now.hour)

                next_refresh = now.replace(hour=refresh_in, minute=10, second=15)

                wait = (next_refresh - now).seconds
                await asyncio.sleep(wait)
