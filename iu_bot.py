#usr/bin/env python3.6
# -*- coding: utf-8 -*-


from discord.ext import commands
import discord

from time import localtime, strftime
import os
from exts.cogs import globalvars
from exts.cogs.CustomAiopg import aiopg_commands #used to handle database
import time, datetime
import random
import gspread


bot = commands.Bot(description='IU Bot Dev build', command_prefix=['dev ', 'iu_dev '])


ownerid = {360022804357185537: "Pegasus",
            315728369369088003: "Ekansh", 
            270898185961078785: "Shirious", 
            341958485724102668: "UniQ", 
            388984732156690433: "Yash", 
            341171182227161088: "Oxide", 
            443961507051601931: "Uday"}

aio = aiopg_commands() #used for database purposes

@bot.event
async def on_ready():

    botLogChannel = await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logID)
    devBotLogChannel = await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logDevID)
    if bot.user.id == 453748284834447361: #iu bot dev 
        devBotLogChannel.send("IU Bot **DEV** load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")
    else:
        botLogChannel.send("IU Bot load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")
           
    await aio.connect()
    await aio.execute("CREATE TABLE IF NOT EXISTS Dailies(id BIGINT, dailiesCount INT, remaining_timestamp TIMESTAMP)")
    await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT)")
    bot.aio = aio
    extentions = ("Admin", "Economy", "Events", "General", "repl", "Miscellaneous")
    for i in extentions:
        try:
            bot.load_extension("exts.cogs.{}".format(i))
        except Exception as e:
            if bot.user.id == 453748284834447361: #iu bot dev 
                devBotLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
            else:
                botLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
    
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="on Indians United [iu_help reveals commands]"))


bot.run(globalvars.TOKEN)
