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
        if reaction.message.channel.id != 567050071628054532 and reaction.message.guild.id == 281793428793196544:
            if ((reaction.emoji == "\u2b50") or (reaction.emoji == "🌟")) and reaction.count > 2:
                message = reaction.message
                async def emsend(stars: int):
                    em = discord.Embed(description=message.content)
                    em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url_as(format='png'))
                    em.timestamp = message.created_at
                    em.add_field(name=None, value=f'[Jump!]({message.jump_url})')
                    emb.color = 0xFFDF00
                    if message.embeds:
                        data = message.embeds[0]
                        if data.type == 'image':
                            em.set_image(url=data.url)
                    if message.attachments:
                        file = message.attachments[0]
                        if file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                            em.set_image(url=file.url)
                        else:
                            em.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)
                    if stars > 2 and stars < 5:
                        staremoji = ":star:"
                    if stars > 3 and stars < 8:
                        staremoji = ":star2:"
                    if stars > 7 and stars < 12:
                        staremoji = ":dizzy:"
                    if stars > 12:
                        staremoji = ":sparkles:"
                    await self.bot.guilds[0].get_channel(567050071628054532).send(content = " %s %s ID:%s"%(staremoji, message.channel, message.id), embed = em)
                emsend(reaction.count)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = await ctx.send("❌ | Sorry, you're on a cooldown, try again in {}s".format(str(int(err.retry_after))))
            await asyncio.sleep(5)
            await msg.delete()

        elif isinstance(err, commands.errors.CommandNotFound) or isinstance(err, commands.errors.CheckFailure):
            pass
        elif isinstance(err, commands.errors.CommandInvokeError):
            stack = 4  # how many levels deep to trace back
            traceback_text = "\n".join(traceback.format_exception(type(err), err, err.__traceback__, stack))
            print(traceback_text)

        else:
            embed=discord.Embed(title=str(type(err))[8:-2],description=str(err),colour=discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            await ctx.send("Command raised an error***",embed=embed,delete_after=15)
            stack = 4  # how many levels deep to trace back
            traceback_text = "\n".join(traceback.format_exception(type(err), err, err.__traceback__, stack))
            print(traceback_text)

def setup(bot):
    bot.add_cog(Events(bot))
