from nextcord import ClientCog
from nextcord.interactions import Interaction
from nextcord.channel import TextChannel
from db.setup import db_setup
from db.channel import create_channel
from sqlalchemy.exc import IntegrityError
from nextcord.ext.commands import Cog
from nextcord.ext import commands
import logging
from nextcord import slash_command


class UserCog(Cog):

    def __init__(self, client, session) -> None:
        self.client = client
        self.session = session
        super().__init__()

    @slash_command(name="start", guild_ids=[932387113335406652])
    async def start(self, inter: Interaction, channel: TextChannel):
        logging.info(f"[Start command] user={inter.user.name}")
        if inter.user.guild_permissions.administrator:
            logging.info(f"[Start command] user={inter.user.name}, channel_id={channel.id}, channel={channel.name}")
            channel = create_channel(self.session, channel_id=channel.id)
            if channel:
                logging.info("[Start command] User successfully created channel!")
                return await inter.response.send_message("Успешно!", ephemeral=True)
            else:
                logging.info("[Start command] User doesn't create channel because channel already exists.")
                return await inter.response.send_message("Этот канал уже зарегистрирован.", ephemeral=True)
        logging.info("[Start command] User doesn't create channel because dont have permission")
        return await inter.response.send_message("Не можно!", ephemeral=True)