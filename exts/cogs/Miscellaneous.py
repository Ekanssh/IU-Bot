#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


class Miscellaneous:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fb'])
    async def feedback(self,ctx,*,message):
        '''Please provide any feedback and report any bugs.'''
        author = ctx.message.author.name + " said in " + "'" + ctx.guild.name + "'"
        await self.bot.get_guild(381052278708240385).get_channel(435375286385770497).send(embed=discord.Embed(color=eval(hex(ctx.author.color.value)),title=author,description="#"+ctx.channel.name+":\n"+message))
        await ctx.message.add_reaction('\u2705')

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
