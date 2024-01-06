from dotenv import dotenv_values
from nextcord import Client
from schedule import stock_subscriber
import asyncio
from nextcord.interactions import Interaction
from nextcord.channel import TextChannel
from db.setup import db_setup
from db.channel import create_channel
from sqlalchemy.exc import IntegrityError
import logging
import sys



TOKEN = dotenv_values().get("TOKEN")
DB_URL = dotenv_values().get("DB_URL")
DEBUG = dotenv_values().get("DEBUG")

bot = Client()

@bot.slash_command(name="start", guild_ids=[1163560736891605042])
async def start(inter: Interaction, channel: TextChannel):
    logging.info(f"[Start command] user={inter.user.name}")
    if inter.user.guild_permissions.administrator:
        logging.info(f"[Start command] user={inter.user.name}, channel_id={channel.id}, channel={channel.name}")
        channel = create_channel(bot.session, channel_id=channel.id)
        if channel:
            logging.info("[Start command] User successfully created channel!")
            return await inter.response.send_message("Успешно!", ephemeral=True)
        else:
            logging.info("[Start command] User doesn't create channel because channel already exists.")
            return await inter.response.send_message("Этот канал уже зарегистрирован.", ephemeral=True)
    logging.info("[Start command] User doesn't create channel because dont have permission")
    return await inter.response.send_message("Не можно!", ephemeral=True)

async def start():

    logging.info("Starting bot...")

    session = db_setup(url=DB_URL)

    await bot.login(token=TOKEN)

    logging.info(f"Bot {bot.user.name} successfully logged in system!")

    bot.session = session

    asyncio.ensure_future(stock_subscriber(bot=bot, session=session))
    
    await bot.connect()


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(start())