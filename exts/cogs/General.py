#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import aiohttp
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw #used in profile command

import time, datetime
from time import localtime, strftime
import random
import os

import asyncio, aiohttp #various needs
from exts.cogs import globalvars


class General:
    '''General commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cricket', 'scores','cric','score'])
    async def cricbuzz(self, ctx) :
        url = "http://www.cricbuzz.com/"
        data = []
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                html = await r.read()
            soup = bs(html, 'html.parser')
        t = soup.find_all(attrs={'class':'cb-ovr-flo'})
        for u in t:
            if u is not None :
                data.append(u.text)
        tossres = data[5]
        inn = [ data[2] , data[4] ]
        tm = [ data[1] , data[3] ]
        curr = data[0]
        em = discord.Embed(title = "{0} vs {1}".format(tm[0],tm[1]) , description = "{5} ... \nCurrent Inning : {0} \n{1} : {2}\n{3} : {4}".format(curr,tm[0],inn[0],tm[1],inn[1],tossres)+"\n*Score Updated at* "+str(strftime("%a, %d %H:%M:%S", localtime())), colour = int(hex(random.randint(0,16777215)),16))
        await ctx.send(embed = em)
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
        tdm = lambda td: ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)
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
    @commands.command(name = '8ball')
    async def _func(self, ctx, *, question = ' '):
        '''the bot entertains you with nonsense'''
        if question[-1] == '?':
            return await ctx.send(random.choice(globalvars.ballAnswers))
        await ctx.send('`Try again with a question!`')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def choose(self, ctx, *, options):
        '''randomly gets a choice from a list of choices separated with '|' '''
        if len(options.split('|')) >= 2:
            return await ctx.send(embed=discord.Embed(title="And the bot has chosen...",description=random.choice(options.split('|')),color=discord.Color.gold()))
        await ctx.send(embed=discord.Embed(title='You invoked command incorrectly!',description='Give at least two options separated by **|**',color=discord.Color.red()))

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def rps(self, ctx, value):
        '''Play Rock Paper Scissors with the bot'''
        options = ['Rock', 'Paper', 'Scissors', 'Rock'];
        value = value.title()
        if value not in options:
            return await ctx.send('You can choose from %s only'%(', '.join(options[:3])))
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
        return await ctx.send('**Bot**: %s\n**You**: %s\n%s'%(guess, value, res))

def setup(bot):
    bot.add_cog(General(bot))
