#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


from discord.ext import commands
import discord

from time import localtime, strftime
import os
import exts.cogs.globalvars
from exts.cogs.CustomAiopg import aiopg_commands #used to handle database
import time, datetime
import random
import gspread


bot = commands.Bot(description='IU Bot Dev build', command_prefix=['dev ', 'iu_dev '])


__ownerid__ = [360022804357185537, 315728369369088003, 270898185961078785, 341958485724102668, 371673235395182592, 388984732156690433]

aio = aiopg_commands() #used for database purposes

@bot.event
async def on_ready():
        await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logID).send("IU Bot **DEV** load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")
        
        await aio.connect()
        await aio.execute("CREATE TABLE IF NOT EXISTS Dailies(id BIGINT, dailiesCount INT, remaining_timestamp TIMESTAMP)")
        await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT)")
        bot.aio = aio
        extentions = ("Admin", "Economy", "Events", "General", "repl", "Miscellaneous")
        for i in extentions:
            try:
                bot.load_extension("exts/cogs/{}".format(i))
            except Exception as e:
                await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logID).send("Erorr occurred in loading {}".format(i) + "\n" + "```{}```".format(e))
        
        

        await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="on Indians United [iu_help reveals commands]"))


bot.run(globalvars.TOKEN)
