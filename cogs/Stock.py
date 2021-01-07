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

    def CheckUserMoney(self, user: str):
        data = self.user.find_one({"_id": user})
        return data["money"]

    def CheckCount(self, user: str, Corporation: int, count: int):
        money = self.CheckUserMoney(user)
        pay = Corporation * count
        if money > pay:
            return True
        return False

    def CorporationBuy(self, user: str, minus: int, Corporation: str, count: int):
        find = {"_id": user}
        data = self.user.find_one(find)
        data["money"] -= minus
        data[Corporation] += count
        setdata = {"$set": data}
        self.user.update_one(find, setdata)

    def CorporationSell(self, user: str, plus: int, Corporation: str, count: int):
        find = {"_id": user}
        data = self.user.find_one(find)
        data["money"] += plus
        data[Corporation] -= count
        setdata = {"$set": data}
        self.user.update_one(find, setdata)

    def NowCorporationPrice(self, Corporation: str):
        find = {"_id": Corporation}
        data = self.coll.find_one(find)
        return data["money"]

    def OldPrice(self, Corporation: str, old: int):
        find = {"_id": Corporation}
        data = self.coll.find_one(find)
        data["old"] = old
        setdata = {"$set": data}
        self.coll.update_one(find, setdata)

    @tasks.loop(seconds=600)
    async def StockLoop(self):
        for i in self.coll.find():
            if i["_id"] == "time":
                return
            self.OldPrice(i["_id"], i["money"])
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
                _id = i["_id"]
                money = i["money"]
                old = i["old"]
                if old < money:
                    now = int(money) - int(old)
                    string += f'+ {i["_id"]} : {i["money"]} : {now} 원 증가\n'
                if old > money:
                    now = int(old) - int(money)
                    string += f'- {i["_id"]} : {i["money"]} : {now} 원 감소\n'

            embed = discord.Embed(title="주식 통계", description=f"```md\n{string}\n```")
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
    async def Buy(self, ctx, Corporation: str, count: int):
        if self.CheckCorporation(Corporation) is Status.OK:
            data = self.coll.find_one({"_id": Corporation})
            now = data["money"]
            if self.CheckCount(str(ctx.author.id), now, count):
                self.CorporationBuy(
                    str(ctx.author.id),
                    self.NowCorporationPrice(Corporation),
                    Corporation,
                    count,
                )
                await ctx.send("구매가 정상적으로 처리 되었습니다! :white_check_mark:")
            else:
                await ctx.send("저런! 돈이 부족해요!")
        else:
            await ctx.send("정상적이지 않은 주식 회사 입니다.")

    @Stock.command(name="팔기")
    @CheckUser()
    async def Sell(self, ctx, Corporation: str, count: int = None):
        if self.CheckCorporation(Corporation) is Status.OK:
            if count == None:
                count = self.user.find_one({"_id": str(ctx.author.id)})[Corporation]
            if self.user.find_one({"_id": str(ctx.author.id)})[Corporation] < count:
                return await ctx.send(
                    f"{str(ctx.author)} 님이 가진 주식이 매도 하시려는것보다 적어 팔수 없어요!"
                )
            data = self.coll.find_one({"_id": Corporation})
            nowprice = self.NowCorporationPrice(Corporation)
            now = nowprice * count
            self.CorporationSell(str(ctx.author.id), now, Corporation, count)
            await ctx.send("정상적으로 처리 되었습니다! :white_check_mark:")

    @Stock.command(name="가방")
    @CheckUser()
    async def Bag(self, ctx):
        find = {"_id": str(ctx.author.id)}
        data = self.user.find_one(find)
        string = str()
        for i in data:
            if i == "_id" or i == "money":
                pass
            else:
                string += f"{i} : {data[i]} 개\n"
        embed = discord.Embed(
            title=f"{str(ctx.author)} 님의 주식 가방", description=f"```\n{string}\n```"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stock(bot))
    print("Stock.py 준비 완료.")