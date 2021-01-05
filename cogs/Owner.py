import discord
from discord.ext import commands
from config import OWNERS
import ast


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNERS

    return commands.check(predicate)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def eval(self, ctx, *, cmd):
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                "bot": self.bot,
                "discord": discord,
                "commands": commands,
                "ctx": ctx,
                "__import__": __import__,
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = await eval(f"{fn_name}()", env)
            await ctx.send(result)
        except Exception as a:
            await ctx.send(a)


def setup(bot):
    bot.add_cog(Owner(bot))
    print("Owner.py 준비 완료.")
