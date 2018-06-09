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
    async def profile(self, ctx, mem: discord.Member = None):
        '''Check your or someone else's profile'''
        found = False
        mem = mem or ctx.message.author
        if mem.bot:
            await ctx.send("Sorry, bots don't have a profile...")
            return

        
        await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id, ))
        for i in await self.bot.aio.cursor.fetchall():
            if i is not None:
                if i[0] == mem.id:
                    found = True
                    await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(mem.id), ))
                    if len(await self.bot.aio.cursor.fetchall()) > 0:
                        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(mem.id), ))
                        currentDaily = int((await self.bot.aio.cursor.fetchall())[0][1])
                    else :
                        currentDaily = 0

                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
                    level = (await self.bot.aio.cursor.fetchall())[0][4]

                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
                    note = (await self.bot.aio.cursor.fetchall())[0][5]

                    back = Image.open("exts/Images/background.png")
                    background = Image.open("exts/Images/milky-way.jpg")
                    background = background.crop((0, 0, 500, 215))
                    back.paste(background, box = (0, 0))
                    font = ImageFont.truetype("exts/Fonts/Quicksand-Regular.otf", 45)
                    badges_font = ImageFont.truetype("exts/Fonts/Quicksand-Regular.otf", 25)
                    level_font = ImageFont.truetype("exts/Fonts/Quicksand-Regular.otf", 25)
                    credits_reps_font = ImageFont.truetype("exts/Fonts/Quicksand-Regular.otf", 20)
                    note_font = ImageFont.truetype("exts/Fonts/Quicksand-Regular.otf", 20)

                    d = ImageDraw.Draw(back)
                    d.rectangle([0, 160, 110, 270], fill = (255, 255, 255))
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(mem.avatar_url) as r:
                            with open("TEMPava.png", 'wb') as ava:
                                ava.write(await r.read())
                    avatar = Image.open("TEMPava.png")
                    avatar = avatar.resize((100, 100))
                    back.paste(avatar, (5, 165))
                    d.text(text = str(mem), xy = (125, 215), font = font)
                    d.line([(113, 219), (113, 500)], fill = (50, 50, 50), width = 3) #line beside ava

                    d.line([(11, 302), (100, 302)], fill = (50, 50, 50), width = 3)
                    d.text(text = "Badges", xy = (10, 275), font = badges_font)
                    d.text(text = "Level:", xy = (360, 265), font = level_font)
                    d.text(text = str(level), xy = (435, 265), font = level_font)

                    d.text(text = "Credits:", xy = (135, 310), font = credits_reps_font)
                    d.text(text = str(currentDaily), xy = (435, 310), font = credits_reps_font, align = 'RIGHT')

                    d.text(text = "Reputations:", xy = (135, 340), font = credits_reps_font)
                    d.text(text = "-", xy = (435, 340), font = credits_reps_font, align = 'RIGHT')

                    d.rectangle([135, 400, 480, 490])
                    d.text(text = note, xy = (145, 405), font = note_font)
                    back.save(str(mem.name) + '.png')
                    await ctx.send(file = discord.File(str(mem.name) + '.png'))
                    os.remove(str(mem.name) + '.png')
                    os.remove('TEMPava.png')

        if not found:
            await self.bot.aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s)", (mem.id, 0, 'milky-way', 'None', 1, 'I am imperfectly perfect...', 0))
            await ctx.invoke(self.bot.get_command("profile"), mem)


    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def note(self, ctx, option="show", *, newNote = None):
        '''Set your profile's note'''
        if ctx.message.author.bot:
            return
        if option == "show":
            await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.message.author.id,))
            note =  (await self.bot.aio.cursor.fetchall())[0][5]
            await ctx.send("Your current note is:\n" + "```" + note + "```")
        elif option == "set" and newNote is not None:
            await self.bot.aio.execute("UPDATE profile SET note = %s WHERE id = %s", (newNote, ctx.message.author.id, ))
            await ctx.send("Your current note is:\n" + "```" + newNote + "```")
        elif option == "reset":
            await self.bot.aio.execute("UPDATE profile SET note = %s WHERE id = %s", ('I am imperfectly perfect...', ctx.message.author.id, ))
            await ctx.send("Your profile's note has been reset to:\n" + '```I am imperfectly perfect...```')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def rep(self, ctx, mem:discord.Member):
        if ctx.author.bot or mem.bot:
            return
        if ctx.author.id is mem.id:
            await ctx.send("You can not give reputation point to yourself.")
        found_author = False
        found_mem = False
        await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (ctx.message.author.id, ))
        for i in await self.bot.aio.cursor.fetchall():
            if i is not None:
                found_author = True
        await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (mem.id, ))
        for i in await self.bot.aio.cursor.fetchall():
            if i is not None:
                found_mem = True
        if found_author and found_mem:
            await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (mem.id, ))
            currentRep = int((await self.bot.aio.cursor.fetchall())[0][1])
            await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (ctx.message.author.id, ))
            repFlag = (await self.bot.aio.cursor.fetchall())[0][2]
            if repFlag is "False":
                await ctx.send("Reputation point already given.")
            else:
                await self.bot.aio.execute("UPDATE rep SET flag = %s WHERE id = %s", ('True', ctx.message.author.id, ))
                await self.bot.aio.execute("UPDATE rep SET reps = %s WHERE id = %s", (currentRep + 1, mem.id, ))
                await ctx.send("You have given reputation point to " + mem.mention)
        elif found_author:
            await self.aio.execute("SELECT * FROM rep WHERE id = %s", (ctx.message.author.id, ))
            repFlag = (await self.bot.aio.cursor.fetchall())[0][2]
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 1, 'False')", (mem.id, ))
            if repFlag is "False":
                await ctx.send("Reputation point already given.")
            else:
                await self.bot.aio.execute("UPDATE rep SET flag = %s WHERE id = %s", ('True', ctx.message.author.id, ))
                await ctx.send("You have given reputation point to " + mem.mention)
        elif found_mem:
            await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (mem.id, ))
            currentRep = int((await self.bot.aio.cursor.fetchall()))[0][1]
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 0, 'True')", (ctx.message.author.id, ))
            await self.bot.aio.execute("UPDATE rep SET reps = %s WHERE id = %s", (currentRep + 1, mem.id, ))
            await ctx.send("You have given reputation point to " + mem.mention)
        else:
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 0, 'True')", (ctx.message.author.id, ))
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 1, 'False')", (mem.id, ))
            await ctx.send("You have given reputation point to " + mem.mention)

    '''
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def top(self, ctx):
        #Check who tops the local server's Scoreboard
        msg = await ctx.send("*Please wait until I gather people's information*")
        page_index = 1
        embed_list = []
        await aio.execute("SELECT id, xp FROM profile")
        rows_count = len(await aio.cursor.fetchall())
        row_index = 1
        async with aiopg.create_pool(dsn) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as c:
                    await c.execute("SELECT id, xp FROM profile ORDER BY xp DESC LIMIT %s OFFSET %s", (10, 10-10))
                    for l in await c.fetchall():
                        name = (await self.bot.get_user_info(l[0])).name
                        await ctx.send(name)


        for i in range (10, rows_count, 10):
            await aio.execute("SELECT id, xp FROM profile ORDER BY xp DESC LIMIT %s OFFSET %s", (i, i-10))
            em = discord.Embed(title = "Scoreboard for " + ctx.guild.name,
                                    color = 0x00FFFF,
                                    description = '')
            position = 0
            for l in await aio.cursor.fetchall():
                try:
                    name = (await self.bot.get_user_info(l[0])).name
                    em.description += name + ' ' * (29 - len(name)) + ':: ' + str(l[6]) + '\n'
                    if l[0] == ctx.message.author.id:
                        position = row_index
                    row_index += 1
                except:
                    em.description += "Couldn't find user. Discord id: `{}`".format(l[0])
            em.add_field(name = ctx.message.author.name, value = "\n\nYour position in " + ctx.guild.name + " is " + str(position))
            em.set_footer(text="Page {0} of {1}".format(page_index, int(rows_count/10)))
            page_index += 1
            embed_list.append(em)


        info_embed = discord.Embed(title = "Help Info",
                                   description = "\u23EA:  Go to the first page\n\u25C0:  Go to the previous page\n\u23F9:  Stop the help command\n\u25B6:  Go to the next page\n\u23E9:  Go to the last page\n\U0001f522:  Asks for a page number\n\u2139:  Shows this info",
                                   colour = 0x2279DE)
        embed_list.append(info_embed)
        await msg.edit(embed = embed_list[0])
        pa = Paginator(self.bot, msg, ctx.message.author, 0)
        await pa.paginate(embed_list)
    '''

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def ping(self, ctx):
        '''Call the bot'''
        msg = await ctx.send(ctx.author.mention+', Pong!')
        res = msg.created_at - ctx.message.created_at
        tdm = lambda td: ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)
        res = tdm(res)
        await msg.edit(content=ctx.author.mention+', Pong! :ping_pong: Took {} ms'.format(res))

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
        '''The bot entertains you with nonsense'''
        if question[-1] == '?':
            return await ctx.send(random.choice(globalvars.ballAnswers))
        await ctx.send('`Try again with a question!`')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def choose(self, ctx, *, options):
        '''Randomly gets a choice from a list of choices separated with '|' '''
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
