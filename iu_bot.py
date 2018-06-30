#!/usr/bin/python
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord


from time import localtime, strftime
import os
from exts.cogs import globalvars
from exts.cogs.CustomAiopg import aiopg_commands  # used to handle database
import time
import datetime
import random
import json

with open("config.json") as fp:
    config = json.load(fp)

prefixes = config['prefix'].split('|')
maintenance = config['maintenance'] == "True"

if maintenance:
    bot = commands.Bot(description='IU Bot Dev build', command_prefix=prefixes)
else:
    bot = commands.Bot(
        description='The official bot overwatching Indians United discord server.', command_prefix=prefixes)


ownerid = {315728369369088003: "Ekansh",
           270898185961078785: "Shirious",
           388984732156690433: "Yash",
           443961507051601931: "Uday"}

aio = aiopg_commands()  # used for database purposes


@bot.event
async def on_ready():

    botLogChannel = bot.get_guild(
        globalvars.devServerID).get_channel(globalvars.logID)
    devBotLogChannel = bot.get_guild(
        globalvars.devServerID).get_channel(globalvars.logDevID)

    with open("config.json") as fp:
        bot.config = json.load(fp)

    if maintenance:  # To check if the branch is development or not
        await devBotLogChannel.send("IU Bot **DEV** load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")
    else:
        await botLogChannel.send("IU Bot load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")

    await aio.connect()
    await aio.execute("CREATE TABLE IF NOT EXISTS Dailies(id BIGINT PRIMARY KEY, dailiesCount INT, remaining_timestamp TIMESTAMP)")
    await aio.execute("CREATE TABLE IF NOT EXISTS rep(id BIGINT PRIMARY KEY, reps INT, last_given TIMESTAMP)")
    await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT PRIMARY KEY, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT, banners_buyed TEXT)")

    bot.aio = aio
    extentions = ("Admin", "Economy", "Events", "General",
                  "repl", "Miscellaneous", "Profile")
    for i in extentions:
        try:
            bot.load_extension("exts.cogs.{}".format(i))
        except Exception as e:
            if maintenance:  # iu bot dev
                await devBotLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
            else:
                await botLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))

    await bot.change_presence(status=discord.Status.dnd,
                              activity=discord.Game(name="on Indians United [iu_help reveals commands]"))


bot.run(str(os.environ['TOKEN']))
