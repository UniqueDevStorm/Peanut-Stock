import discord
from discord.ext import commands
from pymongo import MongoClient
from tools.Eco import Eco
from config import OWNERS

client = MongoClient("mongodb://localhost:27017/")
coll = client.peanut.user


def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNERS

    return commands.check(predicate)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = client
        self.coll = coll

    @commands.command(name="돈")
    async def Money(self, ctx):
        data = self.coll.find_one({"_id": str(ctx.author.id)})
        embed = discord.Embed(
            title=f"{str(ctx.author)}",
            description=f":money_with_wings: {data['money']}",
        )
        await ctx.send(embed=embed)

    @commands.command(name="가입")
    async def Register(self, ctx):
        if self.coll.find_one({"_id": str(ctx.author.id)}):
            return await ctx.send("앗! 벌써 가입하셨네요!")
        user = Eco(self.coll, str(ctx.author.id))
        user.init()
        await ctx.send("가입이 정상적으로 완료되었습니다! :white_check_mark:")

    @commands.command(name="탈퇴")
    async def Secession(self, ctx):
        if self.coll.find_one({"_id": str(ctx.author.id)}):
            user = Eco(self.coll, str(ctx.author.id))
            user.delete()
            return await ctx.send("탈퇴가 정상적으로 완료되었습니다! :white_check_mark:")
        await ctx.send("가입된 계정을 찾을수 없습니다.")

    @commands.group()
    @is_owner()
    async def SystemCall(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @SystemCall.command()
    async def GetMoney(self, ctx, money: int):
        find = {"_id": str(ctx.author.id)}
        data = self.coll.find_one(find)
        data["money"] = money
        setdata = {"$set": data}
        self.coll.update_one(find, setdata)


def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy.py 준비 완료.")