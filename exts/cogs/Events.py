#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
All bot events here pls :-)

Except the on_ready event because it is needed to lead other extentions
"""

from discord.ext import commands
import discord 
import string #needed for counting channel
import globalvars
import asyncio, aiohttp #various needs

def calculate_level(level: 'current level') -> 'xp to reach next level':
            return (level**2+level)/2*100-(level*100)
  

class Events:

	def __init__(self, bot):
		self.bot = bot

	
	@self.bot.event
	async def on_member_join(member):
	    if member.guild.id == 281793428793196544:
	        channel = self.bot.get_channel(429618676875001856)
	        await channel.send('Welcome to Indians United, '+member.mention+'! Please enjoy your time here and hope you check #rules! :)')

	@self.bot.event
	async def on_member_remove(member):
	    if member.guild.id == 281793428793196544:
	        channel = bot.get_channel(429618676875001856)
	        await channel.send('We are feeling bad to see you leaving %s!' %(member.name))

	@self.bot.event
	async def on_message(msg):
	    if msg.channel.id == 434664516991844352: #counting channel
	        last_nos = []
	        async for i in msg.channel.history(limit=2):
	            try:
	                number = int(i.content)
	                last_nos.append(number)
	            except:
	                await msg.delete()
	        if last_nos[0] != last_nos[1]+1 :
	            await msg.delete()
	    
	    if msg.channel.name is globalvars.memesChannel:
	        for chr in list(string.ascii_letters):
	            if chr in str(msg.content):
	                await msg.delete()

	    found = False
	    if not msg.author.bot:
	        await aio.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
	        for i in await aio.cursor.fetchall():
	            if i is not None:
	                if i[0] == msg.author.id:

	                    found = True

	                    await aio.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
	                    xp = (await aio.cursor.fetchall())[0][6]
	                    await aio.execute("UPDATE profile SET xp = %s WHERE id = %s", (xp + 5, msg.author.id, ))

	                    await aio.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
	                    level = (await aio.cursor.fetchall())[0][4]

	                    if xp == int(calculate_level(level)):
	                        await aio.execute("UPDATE profile SET level = %s WHERE id = %s", (level + 1, msg.author.id, ))
	                        await msg.channel.send("Congratulations, " + msg.author.mention + " you advanced to level {}".format(level + 1),delete_after=10)
	    if not found:
	        if not msg.author.bot:
	            await aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s)", (msg.author.id, 0, 'milky-way', 'None', 1, 'I am imperfectly perfect...', 0))

	    await bot.process_commands(msg)

	@self.bot.event
	async def on_message_edit(before, after):
	    await self.bot.process_commands(after)

def setup(bot):
	bot.add_cog(Events(bot))