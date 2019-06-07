#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import aiohttp

banned = {367740727624466433: "Karan",
          341171182227161088: "Oxide"}

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fb', 'suggest'])
    async def feedback(self, ctx, *, message):
        '''Please provide any feedback and report any bugs.'''
        if ctx.author.id not in banned:
            author = ctx.message.author.name + " said in " + "'" + ctx.guild.name + "'"
            await self.bot.get_guild(381052278708240385).get_channel(435375286385770497).send(embed=discord.Embed(color=eval(hex(ctx.author.color.value)), title=author, description="#"+ctx.channel.name+":\n"+message))
            await ctx.message.add_reaction('\u2705')
        else:
            await ctx.send("Not allowed.")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
