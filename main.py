from dotenv import dotenv_values
from nextcord import Client
from schedule import stock_subscriber
import asyncio
from nextcord.interactions import Interaction
from nextcord.channel import TextChannel
from db.setup import db_setup
from db.channel import create_channel
from sqlalchemy.exc import IntegrityError


TOKEN = dotenv_values().get("TOKEN")
DB_URL = dotenv_values().get("DB_URL")

bot = Client()


@bot.slash_command(name="start", guild_ids=[1163560736891605042])
async def start(inter: Interaction, channel: TextChannel):

    if inter.user.guild_permissions.administrator:
        channel = create_channel(bot.session, channel_id=channel.id)
        if channel:
            return await inter.response.send_message("Успешно!", ephemeral=True)
        else:
            return await inter.response.send_message("Этот канал уже зарегистрирован.", ephemeral=True)
    return await inter.response.send_message("Не можно!", ephemeral=True)

async def start():

    session = db_setup(url=DB_URL)

    await bot.login(token=TOKEN)

    bot.session = session

    asyncio.ensure_future(stock_subscriber(bot=bot, session=session))

    await bot.connect()


if __name__ == "__main__":
    asyncio.run(start())