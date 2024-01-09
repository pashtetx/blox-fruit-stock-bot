from dotenv import dotenv_values
from nextcord import Client
from schedule import stock_subscriber
import asyncio
import logging
import sys
from cogs.user_cog import UserCog
from db.setup import db_setup

TOKEN = dotenv_values().get("TOKEN")
DB_URL = dotenv_values().get("DB_URL")
DEBUG = dotenv_values().get("DEBUG")

async def start():

    bot = Client()
    
    logging.info("Starting bot...")
    session = db_setup(url=DB_URL)

    await bot.login(token=TOKEN)
    bot.add_cog(UserCog(bot, session))

    logging.info(f"Bot {bot.user.name} successfully logged in system!")

    stock_subscriber.start(bot=bot, session=session)

    await bot.connect()
    

if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(start())