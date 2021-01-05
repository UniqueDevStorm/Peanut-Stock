import discord
from discord.ext import commands
from tools.Autocogs import AutoCogs
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

TOKEN = os.getenv("TOKEN")


class Peanut(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="./")
        self.remove_command("help")
        AutoCogs(self)

    async def on_ready(self):
        print(f"{self.user.name}#{self.user.discriminator} is Online.")

    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await self.process_commands(message)


bot = Peanut()
bot.run(TOKEN, bot=True)