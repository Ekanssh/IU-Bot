#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import aiohttp
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw  # used in profile command
import googlemaps # used in atlas game

import time
import datetime
from time import localtime, strftime
import random
import os

import asyncio
import aiohttp  # various needs
from exts.cogs import globalvars


class General:
    '''General commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cricket', 'scores', 'cric', 'score'])
    async def cricbuzz(self, ctx):
        url = "http://www.cricbuzz.com/"
        data = []
        async with aiohttp.ClientSession() as cs:
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
        '''Call the bot'''
        msg = await ctx.send('Pong!')
        res = msg.created_at - ctx.message.created_at

        def tdm(td): return ((td.days * 86400000) +
                             (td.seconds * 1000)) + (td.microseconds / 1000)
        res = tdm(res)
        await msg.edit(content='Pong! :ping_pong: Took {} ms'.format(res))

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def say(self, ctx, *, something: commands.clean_content='IU Bot Bot here!'):
        '''The bot becomes your copycat'''
        await ctx.send(something)
        await ctx.message.delete()

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

        self.bot.atlas_active_channels[ctx.channel.id] = [ctx.author, ]

        players_list = []
        for i in range(len(players)):
            mem = await commands.MemberConverter().convert(ctx, players[i])
            if isinstance(mem, discord.Member):
                if mem not in players_list:
                    players_list.append(mem)

        msg = await ctx.send(f"{ctx.author.mention} has invited {', '.join([m.mention for m in players_list])}.\n"
                        "Type `join` to join the game in 30s.")
        def check(m):
            return m.content == 'join' and m.author in players_list and m.author not in self.bot.atlas_active_channels[ctx.channel.id]

        for i in range(len(players_list)):
            try:
                join_msg = await self.bot.wait_for('message', check = check, timeout = 30)
                self.bot.atlas_active_channels[ctx.channel.id].append(join_msg.author)

            except asyncio.TimeoutError:
                self.bot.atlas_active_channels.pop(ctx.channel.id, None)
                return await ctx.send("Sorry, {ctx.author.mention}, no one joined. Maybe try again later?")

        if len(self.bot.atlas_active_channels[ctx.channel.id]) == 1 :
            self.bot.atlas_active_channels.pop(ctx.channel.id, None)
            return await ctx.send("You can't play with yourself!")

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
                    g_maps = googlemaps.Client(key = "AIzaSyAu-p7eW9fiaMdACb4pXwfsTF2hpY7h_1k")
                    place = g_maps.find_place(g_msg.content.strip(), input_type = "textquery")
                    if place['status'] == "OK":
                        turn = 0 if turn == (len(self.bot.atlas_active_channels[ctx.channel.id]) - 1) else turn + 1
                        letter = g_msg.content.strip()[-1]
                        await ctx.send(f"Nice! It's {self.bot.atlas_active_channels[ctx.channel.id][turn].name}'s turn now with the letter `{letter}`. 20s. GO!")
                    else:
                        await ctx.send(f"Sorry, {self.bot.atlas_active_channels[ctx.channel.id][turn].name}, I travelled all around the globe"
                                       f" but could not find the place called {g_msg.content}."
                                        "\nYou're kicked out of the game!")
                        self.bot.atlas_active_channels[ctx.channel.id].pop(turn)                
                        continue
            except asyncio.TimeoutError:
                await ctx.send(f"{str(self.bot.atlas_active_channels[ctx.channel.id][turn])} is kicked out of the game because they failed to reply before 20s")
                self.bot.atlas_active_channels[ctx.channel.id].pop(turn)             
                continue

        await ctx.send(f"{self.bot.atlas_active_channels[ctx.channel.id][0].name} wins the game! :tada:")
        self.bot.atlas_active_channels.pop(ctx.channel.id, None)

def setup(bot):
    bot.add_cog(General(bot))
