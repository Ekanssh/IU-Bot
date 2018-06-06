#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


from discord.ext import commands
import discord

from time import localtime, strftime
import os
import ext.cogs.globalvars
from ext.cogs.CustomAiopg import aiopg_commands #used to handle database
import time, datetime
import random


bot = commands.Bot(description='The offical bot overwatching Indians United.', command_prefix=['iu_', 'iu ', 'IU ', 'IU_', 'Iu ','Iu_'])

if creds.access_token_expired:
    client.login()

__ownerid__ = [360022804357185537, 315728369369088003, 270898185961078785, 341958485724102668, 371673235395182592, 388984732156690433]

aio = aiopg_commands() #used for database purposes

@bot.event
    async def on_ready(self):
        await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logID).send("Bot load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")
        
        await aio.connect()
        await aio.execute("CREATE TABLE IF NOT EXISTS Dailies(id BIGINT, dailiesCount INT, remaining_timestamp TIMESTAMP)")
        await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT)")
        bot.aio = aio
        extentions = ("Admin", "Economy", "Events", "General", "repl", "Miscellaneous")
        for i in extentions:
            try:
                bot.load_extension("exts/cogs/{}".format(i))
            except Exception as e:
                await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logID).send("Erorr occurred in loading {}".format(i))
        
        

        await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="on Indians United [iu_help reveals commands]"))

        async def dbauth():
            while True:
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
                http = creds.authorize(httplib2.Http())
                creds.refresh(http)
                client = gspread.authorize(creds)
                if creds.access_token_expired:
                    client.login()
                await asyncio.sleep(3000)
        bot.loop.create_task(dbauth())



bot.run(globalvars.TOKEN)
