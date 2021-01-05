import discord
from discord.ext import commands
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Core(bot))
    print("Core.py 준비 완료.")
