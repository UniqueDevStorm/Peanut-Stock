import discord
import random
from discord.ext import commands
from discord.ext import tasks
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
coll = client.peanut.stock


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client
        self.coll = coll

    def NextPrice(self, now):
        r = random.randint(1, 2)
        ran = random.randint(1, 500)
        if int(r) == 1:  # -로 정함
            result = now - ran
            if result <= 0:
                result = now + ran
        if int(r) == 2:  # + 로 정함
            result = now + ran
        return result

    @commands.command()
    async def Test(self, ctx):
        string = list()
        for i in self.coll.find():
            Next = self.NextPrice(i["money"])
            i["money"] = Next
            string.append(i)
        await ctx.send(string)


def setup(bot):
    bot.add_cog(Stock(bot))
    print("Stock.py 준비 완료.")