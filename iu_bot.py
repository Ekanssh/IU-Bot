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
import googlemaps # used in atlas game


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
    bot.atlas_active_channels = {}
    bot.g_maps = googlemaps.Client(key = "\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDbrjONd+Dke4QG\n2VS29BTPiPPCUaAO526Ml4ZooR/19A26nPRe3js3W69CrMinNGtLdWyYrnnKzHR26vu4cv/cfzt/DTeQUB0Xl8UbREc7oywT08JI6Jm5zBLZTSXgi164MCGG3u5RKXaBGVBabmxQenPMJNuqUwhg5W8UMFs66YBXrBVhhZzMFLiYk15Wau0P+YLZTSXgi164MCGG3u5RKXaBGVBabmxQTVRAAVE5sc09m4jPlDV1Mq+P83JxAhftYYWAKla0Gk2C6ZZIVv\nZD+BHoo6J6OkAwaPEsOO/GujPM+b54Aadm7lNp//BZE/qqoDE+8IQenPMJNuqUwhg5W8UMFs66YBXrBVhhZzMFTVRAAVEw9tJ4qbh2CCPSXgi164MCGG3u5RKXaBGVBabmxQTVRAAVE1tDTPSEWY5+7r6SxyU988F6PN3YrNS0NtW46fhJ7X/FHURehILMw+pUJy\nyASALqQmJtgAHHO+yeEktBX9o+XKAypMkcTXokUOgMiwpRnPyF3LGVBSt+HftBLZTSDixVHjTGXffS41y2HPDkCqQhu5yRJVbm+lqR7J7BcSkay7cwJ1jHvBnO/YwkVnMY\nGKetsDyjBOJJKyRYe3Gb+VYGW9NjbqhCLltPeljjL7Wo88T6F1pbHjYdqi+AXMK/\ndnDwa8zhmuuwPVRMfsexp/jSXgi164MCGG3u5RKXaBGVBabmxQTVRAAVE5tDT5VtDTqPaP+doh6q/Re3js3W69CrMinNGtLdWyYrnnKzHR26vu4YVtDTF0EwY9I7c5oCBO\nBdu4jfGWefqQ/QBVnGu0Q/1prCnyu0wETZzMPtcYWARbx0LgUhjDk5Hlf4KX7OHi\nahuQuLmrtSpb+GL6jrGF8kKXvvmYtT4zNGqicXRjvuAnmmbvPZXPSEWY5TJeEuqjoHcLiYk15yRJVhA+YlcVBLZTSXgi164MCGG3u5RKXaBGVBabmxQTVRAAVE5tDTZzMFgx9R2xvWauTq0YLT2pY4L8lQbmI9LdVn+LZTSXgi164MCGG3u5RKXaBGVBabmxQenPMJNuqUwhg5W8UMFs66YBXrBVhhZzMFLiYk1d+31W4/9+JES7YdUmuET5FWa1Ich6s0\nT1430FvNdccza/oondIOZl/WhJOcLt+Q5wjbnwfMVLbxd5B9fcIbAMXeZD8t7t4+\ndKYUoN19A26nPRe3js3W69CrGF8kKXvvmYtT4zNGqicXRjvuAnmmbvPZXu5yRJVP\n+JqrxTJNgGpAop/DqWD8ZkBtBj4WkEXdcWK5ePVYDQgx9R2xvWau+At2gwopg3cK\n3uhb4nomYQhcegm2LwHqcDIAvFbfR/hO8hF3qsHol9AVakpy3JCpmjJ2QzviNbKl\nnCRudAws0UEc8zHg4rbInGiM609WPwosr3r1/Z8anQKBgBGK+8oXTLa07aVlc3Ig\nZg0SVikgQZNqW8QZNayFA+SFT/fauKRhtS2eDHyA3n/l19A26AtUGAHt5oyuk4wPi3bXr2gZcVYepeipjq37JK9cLiYk1BV1nZ7udiFr6MNqj3PGR4PGXzCGYQw7UemxRoRxCC97qyJPEg")
    extentions = ("Admin", "Economy", "Events", "General",
                  "repl", "Miscellaneous", "Profile","Roles")
    for i in extentions:
        try:
            bot.load_extension("exts.cogs.{}".format(i))
        except Exception as e:
            if maintenance:  # iu bot dev
                await devBotLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
            else:
                await botLogChannel.send("Erorr occurred in loading {}".format(i) + ":\n" + "```{}```".format(e))
    bot._memList = {}
    for m in bot.users:
        bot._memList[m.id] = m.name
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="on IU | IU help"))


bot.run(str(os.environ['TOKEN']))
