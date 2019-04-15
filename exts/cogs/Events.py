#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
All bot events here pls :-)

Except the on_ready event because it is needed to lead other extentions
"""

from discord.ext import commands
import discord
import string  # needed for counting channel
from exts.cogs import globalvars
import asyncio
import aiohttp  # various needs
import aiopg
import os
import random
import traceback

def calculate_level(level: 'current level') -> 'xp to reach next level':
    return (level**2+level)/2*100-(level*100)


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 281793428793196544:
            channel = self.bot.get_channel(429618676875001856)
            await channel.send('Welcome to Indians United, '+member.mention+'! Please enjoy your time here and hope you check #rules! :)')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 281793428793196544:
            channel = self.bot.get_channel(429618676875001856)
            await channel.send('We are feeling bad to see you leaving %s!' % (member.name))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id == 434664516991844352:  # counting channel
            last_nos = []
            async for i in msg.channel.history(limit=2):
                try:
                    number = int(i.content)
                    last_nos.append(number)
                except:
                    await msg.delete()
            if last_nos[0] != last_nos[1]+1:
                await msg.delete()

        if msg.channel.name is globalvars.memesChannel:
            for chr in list(string.ascii_letters):
                if chr in str(msg.content):
                    await msg.delete()

        found = False
        if not msg.author.bot:
            dsn = 'dbname=' + str(os.getenv('DATABASE')) + ' user=' + str(os.getenv('USER')) + \
                ' password=' + str(os.getenv('PASSWORD')) + \
                ' host=' + str(os.getenv('HOST'))
            async with aiopg.create_pool(dsn) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
                        l = await cur.fetchall()
            for i in l:
                if i is not None:
                    if i[0] == msg.author.id:

                        found = True
                        xp = l[0][6]
                        level = l[0][4]
                        async with aiopg.create_pool(dsn) as pool:
                            async with pool.acquire() as conn:
                                async with conn.cursor() as cur:
                                    await cur.execute("UPDATE profile SET xp = %s WHERE id = %s", (xp + 5, msg.author.id, ))
                                    if xp == int(calculate_level(level)):
                                        await cur.execute("UPDATE profile SET level = %s WHERE id = %s", (level + 1, msg.author.id, ))
                                        await msg.channel.send("Congratulations, " + msg.author.mention + " you advanced to level {}".format(level + 1), delete_after=10)
        if not found:
            if not msg.author.bot:
                await self.bot.aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (msg.author.id, 0, 'banner-9', 'None', 1, 'I am imperfectly perfect...', 0, 'banner-9'))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji in [":star:",":star2:"]:
            if reaction.count == 3 or user.name == "Yashh":
                em = discord.Embed(title = reaction.message.author.name, 
                                   colour = 0xFFDF00, 
                                   description = reaction.message.content)
                em.set_footer(text = "Sent in " + reaction.message.channel.name, 
                              icon_url = reaction.message.author.avatar_url)
                await bot.get_guild(281793428793196544).get_channel(567050071628054532).send(embed=em)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = await ctx.send("❌ | Sorry, you're on a cooldown, try again in {}s".format(str(int(err.retry_after))))
            await asyncio.sleep(5)
            await msg.delete()

        elif isinstance(err, commands.errors.CommandNotFound) or isinstance(err, commands.errors.CheckFailure):
            pass

        else:
            embed=discord.Embed(title=str(type(err))[8:-2],description=str(err),colour=discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            await ctx.send("Command raised an error***",embed=embed,delete_after=15)
            stack = 4  # how many levels deep to trace back
            traceback_text = "\n".join(traceback.format_exception(type(err), err, err.__traceback__, stack))
            print(traceback_text)

def setup(bot):
    bot.add_cog(Events(bot))
