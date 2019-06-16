#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import aiohttp
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw  # used in profile command
import urllib.parse

import time
import datetime
from time import localtime, strftime
import random
import os

import asyncio
import aiohttp  # various needs
from exts.cogs import globalvars
#import urllib.request as ur

from paginator import *

class General(commands.Cog):
    '''General commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cricket', 'scores', 'cric', 'score'])
    async def cricbuzz(self, ctx):
        url = "http://www.cricbuzz.com/"
        data = []
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'cache-control' : 'no-cache'
        }
        #req = ur.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
        #r= ur.urlopen(req)
        async with aiohttp.ClientSession(headers=headers) as cs:
            async with cs.get(url) as r:
                html = await r.read()
        soup = bs(html, 'html.parser')
        t = soup.find_all(attrs={'class': 'cb-ovr-flo'})
        for u in t:
            if u is not None:
                data.append(u.text)
        tossres = data[5]
        inn = [data[2], data[4]]
        tm = [data[1], data[3]]
        curr = data[0]
        em = discord.Embed(title="{0} vs {1}".format(tm[0], tm[1]), description="{5} ... \nCurrent Inning : {0} \n{1} : {2}\n{3} : {4}".format(
            curr, tm[0], inn[0], tm[1], inn[1], tossres)+"\n*Score Updated at* "+str(strftime("%a, %d %H:%M:%S", localtime())), colour=int(hex(random.randint(0, 16777215)), 16))
        await ctx.send(embed=em)
    '''
    @commands.command(aliases = ['scoretable','ipltable','ipl_table','points','points_table','pt'])
    async def pointstable(self, ctx) :
        """Displays the IPL Points Table """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://www.cricbuzz.com//cricket-series/2676/indian-premier-league-2018/points-table") as r:
                data = await r.read()
        soup = bs.BeautifulSoup(data.text,"html.parser")
        data,tmd = [],[]
        teams = ['Delhi Daredevils','Royal Challengers Bangalore','Rajasthan Royals','Kolkata Knight Riders','Mumbai Indians','Chennai Super Kings','Sunrisers Hyderabad','Kings XI Punjab']
        i = 0
        for link in soup.find_all('td') :
            data.append(link.text)
        for i in range(len(data)) :
            if data[i] in teams :
                if len(data[i+1]) <= 2 :
                    x = []
                    for j in range(8) :
                        x.append(data[i+j])
                    tmd.append(x)
        table = ""
        for t in tmd :
            rank = str(tmd.index(t)+1)
            name,plyed,won,lost,points,NRR = t[0],t[1] , t[2] , t[3] , t[-2] , t[-1]
            table += str("\n"+rank + ") " + name + "\n\tP : " + plyed + "\t\tW : "+won+"\t\tL : "+lost+"\n\tP : "+points+"\t\tNRR = "+NRR)
        em = discord.Embed(title = "Points Table IPL 2018" , description = table , colour = int(hex(random.randint(0,16777215)),16) )
        await ctx.send(embed = em )
        '''

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def ping(self, ctx):
        '''checks the time taken for the bot to respond'''
        start = time.monotonic()
        msg = await ctx.send("Pinging... 🕒")
        millis = (time.monotonic() - start) * 1000
        heartbeat = ctx.bot.latency * 1000
        await msg.edit(content=f'Heartbeat: {heartbeat:,.2f}ms Response: {millis:,.2f}ms. ⏲️')


    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def now(self, ctx):
        '''Get current date and time'''
        m = str(datetime.datetime.now()).split()
        embed = discord.Embed(title='Date-time information',
                              color=eval(hex(ctx.author.color.value)))
        embed.add_field(name='Date', value='{}'.format(m[0]))
        embed.add_field(name='Time', value='{}GMT'.format(m[1]))
        await ctx.send(embed=embed)

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(name='8ball')
    async def _func(self, ctx, *, question=' '):
        '''the bot entertains you with nonsense'''
        if question[-1] == '?':
            return await ctx.send(random.choice(globalvars.ballAnswers))
        await ctx.send('`Try again with a question!`')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def choose(self, ctx, *, options):
        '''randomly gets a choice from a list of choices separated with '|' '''
        if len(options.split('|')) >= 2:
            return await ctx.send(embed=discord.Embed(title="And the bot has chosen...", description=random.choice(options.split('|')), color=discord.Color.gold()))
        await ctx.send(embed=discord.Embed(title='You invoked command incorrectly!', description='Give at least two options separated by **|**', color=discord.Color.red()))

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def rps(self, ctx, value):
        '''Play Rock Paper Scissors with the bot'''
        options = ['Rock', 'Paper', 'Scissors', 'Rock']
        value = value.title()
        if value not in options:
            return await ctx.send('You can choose from %s only' % (', '.join(options[:3])))
        guess = random.choice(options[:3])
        i = options.index(value)
        if value is guess:
            res = 'It\'s a tie!'
        elif value == "Rock" and guess == "Rock":
            res = "It's a tie!"
        else:
            if guess is options[i+1]:
                res = 'You lost'
            else:
                res = 'You won'
        return await ctx.send('**Bot**: %s\n**You**: %s\n%s' % (guess, value, res))


    @commands.command()
    async def atlas(self, ctx, *players):
        '''Group atlas game'''
        if ctx.channel.id in self.bot.atlas_active_channels:
            return await ctx.send("Sorry, someone is playing atlas in this channel.\n"
                                  "Please start a new game after they finish or go in another channel")

        if len(players) == 0:
            return await ctx.send("Invite some people to play!")

        self.bot.atlas_active_channels[ctx.channel.id] = [ctx.author, ]

        players_list = []
        cities_named = []
        url = "http://api.openweathermap.org/data/2.5/weather?q="
        for i in range(len(players)):
            try:
                mem = await commands.MemberConverter().convert(ctx, players[i])
                if isinstance(mem, discord.Member):
                    if mem not in players_list:
                        players_list.append(mem)
            except commands.errors.BadArgument:
                if len(players_list) == 0:
                    await ctx.send("No person you asked to join was found in the server. Closing the game.")
                    self.bot.atlas_active_channels.pop(ctx.channel.id, None)

        msg = await ctx.send(f"{ctx.author.mention} has invited {', '.join([m.mention for m in players_list])}.\n"
                        "Type `join` to join the game in 30s.")
        def check(m):
            return m.content == 'join' and m.author in players_list and m.author not in self.bot.atlas_active_channels[ctx.channel.id]

        first_join_msg = datetime.datetime.now()
        while ((datetime.datetime.now() - first_join_msg).total_seconds() <= 30) and len(self.bot.atlas_active_channels[ctx.channel.id]) < (len(players_list)+1):
            try:
                join_msg = await self.bot.wait_for('message', check = check, timeout = int(30-(datetime.datetime.now() - first_join_msg).seconds))
                self.bot.atlas_active_channels[ctx.channel.id].append(join_msg.author)
            except asyncio.TimeoutError:
                if len(self.bot.atlas_active_channels[ctx.channel.id]) < 2:
                    self.bot.atlas_active_channels.pop(ctx.channel.id, None)
                    return await ctx.send(f"Sorry, {ctx.author.mention}, no one joined. Maybe try again later?")

        turn = 0
        letter = "s"
        await ctx.send("An atlas game has started with the following members:\n"+'\n'.join(map(str, self.bot.atlas_active_channels[ctx.channel.id])))
        await ctx.send("Every player gets 20s to say the name of a city, district, state, country, "
                       "basically anything which can be found on the globe.")
        await ctx.send("If someone is unable to do so, they are kicked out of the game.\nGame continues"
                       " until only 1 person is left which will hence be the winner.")
        await ctx.send("First letter is `s`. Reply in 20s!")

        def game_check(m):
            return m.author.id == self.bot.atlas_active_channels[ctx.channel.id][turn].id

        while len(self.bot.atlas_active_channels[ctx.channel.id]) > 1:
            try:
                g_msg = await self.bot.wait_for('message', check = game_check, timeout = 20)

                if g_msg.content[0].lower() == letter:
                    word = urllib.parse.quote_plus(g_msg.content)

                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url + word + "&APPID=" + self.bot.appid) as r:
                            resp = await r.json()

                    if resp['cod'] == 200:
                        if g_msg.content in cities_named:
                            ctx.send(f"Sorry, {ctx.author.mention}, {g_msg.content} has already been said."
                                      "\nYou're kicked out of the game!")
                            self.bot.atlas_active_channels[ctx.channel.id].pop(turn)
                            continue
                        else:
                            turn = 0 if turn == (len(self.bot.atlas_active_channels[ctx.channel.id]) - 1) else turn + 1
                            letter = g_msg.content.strip()[-1]
                            cities_named.append(g_msg.content)
                            await ctx.send(f"Nice! It's {self.bot.atlas_active_channels[ctx.channel.id][turn].mention}'s"
                                           f" turn now with the letter `{letter}`.\nYou have 20s. GO!")
                    else:
                        await ctx.send(f"Sorry, {self.bot.atlas_active_channels[ctx.channel.id][turn].name}, "
                                        "I travelled all around the globe"
                                       f" but could not find the place called {g_msg.content}."
                                        "\nYou're kicked out of the game!")
                        self.bot.atlas_active_channels[ctx.channel.id].pop(turn)
                        if len(self.bot.atlas_active_channels[ctx.channel.id]) > 1:
                            await ctx.send(f"Now it's {self.bot.atlas_active_channels[ctx.channel.id][turn].mention}'s "
                                           f"turn with the letter `{letter}`.\nYou have 20s. GO!")
                        continue
                else:
                    await ctx.send(f"Sorry, {self.bot.atlas_active_channels[ctx.channel.id][turn].mention}, but the word {g_msg.content} does not begin "
                                   f"with the current letter {letter}.\nYou're kicked out of the game!")
                    self.bot.atlas_active_channels[ctx.channel.id].pop(turn)
                    if len(self.bot.atlas_active_channels[ctx.channel.id]) > 1:
                        await ctx.send(f"Now it's {self.bot.atlas_active_channels[ctx.channel.id][turn].mention}'s "
                                       f"turn with the letter `{letter}`.\nYou have 20s. GO!")
                    continue
            except asyncio.TimeoutError:
                await ctx.send(f"{str(self.bot.atlas_active_channels[ctx.channel.id][turn])} is kicked out of "
                                "the game because they failed to reply before 20s")
                self.bot.atlas_active_channels[ctx.channel.id].pop(turn)
                if len(self.bot.atlas_active_channels[ctx.channel.id]) > 1:
                   await ctx.send(f"Now it's {self.bot.atlas_active_channels[ctx.channel.id][turn].mention}'s "
                                  f"turn with the letter `{letter}`.\nYou have 20s. GO!")
                continue

        await ctx.send(f"{self.bot.atlas_active_channels[ctx.channel.id][0].name} wins the game! :tada:")
        self.bot.atlas_active_channels.pop(ctx.channel.id, None)

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.channel)
    async def invite(self,ctx):
        '''Get an invite link to Indians United server'''
        await ctx.send("https://discord.gg/Yn6W84Y")

    @commands.command()
    @commands.has_any_role("Lords", "IU Bot Dev")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.channel)
    async def giveaway(self, ctx, time: int, *, descrip):
        em = discord.Embed(title = "Giveaway by {}! :tada:".format(ctx.author.name),
                                       colour = 0x00ffff,
                                       description = descrip)
        em.set_footer(text = "React to participate.")
        msg = await self.bot.get_guild(281793428793196544).get_channel(587573866554195968).send(embed=em)
        await msg.add_reaction("\U0001F389")
        def check(reaction, user):
            return reaction.emoji is "\U0001F389"
        try:
            await self.bot.wait_for('reaction_add', timeout=time*60*60, check=check)
        except asyncio.TimeoutError:
            msgid = msg.id
            msgg = await self.bot.get_guild(281793428793196544).get_channel(587573866554195968).fetch_message(msgid)
            users = await msgg.reactions[0].users().flatten()
            u = []
            for i in users:
                u.append(i.name)
            u.remove("IU Bot")
            winner = random.choice(u)
            await msg.edit(content = '{} has won the giveaway!'.format(winner), embed=None)

    @commands.command(name='help')
    async def _help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = bot.get_cog(command) or bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(traceback.format_exception(None, e, e.__traceback__))


def setup(bot):
    bot.add_cog(General(bot))
