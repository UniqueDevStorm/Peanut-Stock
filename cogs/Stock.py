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
        self.StockLoop.start()

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

    @tasks.loop(seconds=600)
    async def StockLoop(self):
        for i in self.coll.find():
            Next = self.NextPrice(i["money"])
            find = {"_id": i["_id"]}
            data = self.coll.find_one(find)
            data["money"] = Next
            setdata = {"$set": data}
            self.coll.update_one(find, setdata)


def setup(bot):
    bot.add_cog(Stock(bot))
    print("Stock.py 준비 완료.")