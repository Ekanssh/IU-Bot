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
import calendar
import traceback


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
           443961507051601931: "Uday",
           586426079078514700: "Prometheus"}

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
    await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT PRIMARY KEY, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT, banners_buyed TEXT, score TEXT)")
    await aio.execute("CREATE TABLE IF NOT EXISTS blacklist(id BIGINT PRIMARY KEY)")
    await aio.execute("CREATE TABLE IF NOT EXISTS sar(rolename TEXT PRIMARY KEY)")

    bot.aio = aio
    bot.atlas_active_channels = {}
    bot.appid = "9c23ae0122eeb6cd076c3e2d726312ed"
    extentions = ("Admin", "Economy", "Events", "General",
                  "repl", "Miscellaneous", "Profile", "Roles", "Blacklist", "RaidProtection")
    bot.remove_command('help')
    for i in extentions:
        try:
            bot.load_extension("exts.cogs.{}".format(i))
        except Exception as e:
            await botLogChannel.send("```"+str(traceback.format_exc())+"```")
            if maintenance:  # iu bot dev
                await devBotLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
            else:
                await botLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
    bot._memList = {}
    for m in bot.users:
        bot._memList[m.id] = m.name
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="on IU | IU help"))

    if str(datetime.date.today())[-2:] == '01':
        pass
    if str(calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1]) == str(datetime.date.today())[-2:] and datetime.datetime.now().strftime('%H') == '12':
        pass

@bot.check
async def blacklist_check(ctx):
    await bot.aio.execute("SELECT * from blacklist WHERE id=%s", (ctx.author.id, ))
    l = await bot.aio.cursor.fetchall()
    return True if len(l) == 0 else False

bot.run(str(os.environ['TOKEN']))
