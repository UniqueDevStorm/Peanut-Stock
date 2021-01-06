import discord
import random
from discord.ext import commands
from discord.ext import tasks
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
coll = client.peanut.stock
user = client.peanut.user


class Status:
    class OK:
        pass

    class NotFount:
        pass


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client
        self.coll = coll
        self.user = user
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

    def CheckUser():
        async def check(ctx):
            if user.find_one({"_id": str(ctx.author.id)}):
                return True
            else:
                await ctx.send("가입을 하시지 않았어요! `+가입` 을 사용하여 가입해주세요!")

        return commands.check(check)

    def CheckCorporation(self, string: str):
        if self.coll.find_one({"_id": string}):
            return Status.OK
        return Status.NotFount

    @tasks.loop(seconds=600)
    async def StockLoop(self):
        for i in self.coll.find():
            Next = self.NextPrice(i["money"])
            find = {"_id": i["_id"]}
            data = self.coll.find_one(find)
            data["money"] = Next
            setdata = {"$set": data}
            self.coll.update_one(find, setdata)

    @commands.group(name="주식")
    async def Stock(self, ctx):
        if ctx.invoked_subcommand is None:
            string = str()
            for i in self.coll.find():
                string += f'{i["_id"]} : `{i["money"]}`\n'
            embed = discord.Embed(title="주식 통계", description=string)
            await ctx.send(embed=embed)

    @Stock.command(name="차트")
    @CheckUser()
    async def Chart(self, ctx):
        string = str()
        for i in self.coll.find():
            string += f'{i["_id"]} : `{i["money"]}`\n'
        embed = discord.Embed(title="주식 통계", description=string)
        await ctx.send(embed=embed)

    @Stock.command(name="구매")
    @CheckUser()
    async def Buy(self, ctx, Corporation: str):
        if self.CheckCorporation(Corporation) is Status.OK:
            return await ctx.send("정상적인 주식회사입니다.")
        await ctx.send("정상적이지 않은 주식 회사 입니다.")


def setup(bot):
    bot.add_cog(Stock(bot))
    print("Stock.py 준비 완료.")