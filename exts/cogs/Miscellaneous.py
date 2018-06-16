#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import aiohttp


class Miscellaneous:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fb'])
    async def feedback(self,ctx,*,message):
        '''Please provide any feedback and report any bugs.'''
        author = ctx.message.author.name + " said in " + "'" + ctx.guild.name + "'"
        await self.bot.get_guild(381052278708240385).get_channel(435375286385770497).send(embed=discord.Embed(color=eval(hex(ctx.author.color.value)),title=author,description="#"+ctx.channel.name+":\n"+message))
        await ctx.message.add_reaction('\u2705')

    @commands.command()
    async def weather(self, ctx, *, location):
        '''Gives you the weather of a location'''
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://api.tanvis.xyz/weather/{}'.format(location)) as res:
                res = await res.json(encoding = 'utf-8')
        em = discord.Embed(title = "Current weather of {}".format(location),
                            color = 0x00FFFF)
        for i in res:
            if i != 'error':
                em.add_field(name = i, value= res[i])
            else:
                em.title = "Error"
                em.description = "Could not find the location, {}".format(location)
        await ctx.send(embed = em)
    
    @commands.command()
    async def think(self, ctx):
        '''have fun thinking'''
        await ctx.message.delete()
        await ctx.send(discord.utils.get(bot.emojis,name='fidgetthink'))
   
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
