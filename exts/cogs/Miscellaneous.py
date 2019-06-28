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
            await ctx.send("Hello banned noob!")

    @commands.cooldown(rate=1, per=8, type=commands.BucketType.guild)
    @commands.command()
    async def weather(self, ctx, *, location):
        '''to get the weather of a given location'''
        try:
            async with ctx.typing():
                url = "http://api.tanvis.xyz/weather/" + urllib.request.pathname2url(location)
                f = await utils.getjson(url)
                if 'error' in f:
                    await ctx.send(embed=discord.Embed(title="An error occurred",
                                                       description="I could not find your given location",
                                                       colour=discord.Colour.red()))
                else:
                    embed = discord.Embed(title="Weather information gathered", colour=discord.Colour.dark_orange(),
                                          description="Here is your result, " + ctx.author.mention)
                    embed.add_field(name="Location", value=f['name'], inline=False);
                    embed.add_field(name="Temperature in °C", value=f['celsius'])
                    embed.add_field(name="Temperature in °F", value=f['fahrenheit']);
                    embed.add_field(name="Weather", value=f['weather'])
                    embed.add_field(name="Wind Speed", value=f['windSpeed']);
                    embed.set_thumbnail(url=f['icon'])
                    embed.set_footer(text="using **tanvis.xyz** API")
                    await ctx.send(embed=embed)
        except:
            await ctx.send("An error occurred. Please try again.", delete_after=3)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
