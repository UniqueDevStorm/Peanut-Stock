import discord
from discord.ext import commands
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client
        self.mydb = self.client["peanut"]
        self.mycol = self.mydb["stock"]


def setup(bot):
    bot.add_cog(Stock(bot))
    print("Stock.py 준비 완료.")