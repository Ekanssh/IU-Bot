from discord.ext import commands
import discord

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    @commands.has_any_role('Lords', 'IU Bot Dev')
    def blacklist(ctx, mem: discord.Member):
        await self.bot.aio.execute("INSERT INTO blacklist VALUES (%s)", (mem.id, ))
        em = discord.Embed(title = "Blacklisted {}".format(mem.name), colour = 0x000000, description = "Added {} to the blacklist.\n{} cannot use IU Bot anymore.".format(mem.name, mem.name))
        await ctx.send(embed = em)

    @commands.command(hidden = True)
    @commands.has_any_role('Lords', 'IU Bot Dev')
    def whitelist(ctx, mem: discord.Member):
        await self.bot.aio.execute("SELECT * FROM blacklist WHERE id=%s", (mem.id, ))
        l = await self.bot.aio.cursor.fetchall()

        if len(l) == 0:
            return await ctx.send("{} is not in the blacklist :facepalm:".format(mem.name))
        else:
            await self.bot.aio.execute("DELETE FROM blacklist WHERE id=%s", (mem.id, ))
            em = discord.Embed(title = "Whitelisted {}".format(mem.name), colour = 0x00DD00, description = "Removed {} from the blacklist.\nThey can use IU Bot now.".format(mem.name))
            await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Blacklist(bot))