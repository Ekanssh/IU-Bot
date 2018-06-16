#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord 
from exts.cogs.Paginator import Paginator 
from PIL import Image, ImageFont, ImageDraw #used in profile command 
import aiohttp
import os
import json
import asyncio


class Profile:
    def __init__(self, bot):
        self.bot = bot

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
                    await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (mem.id, ))
                    if len(await self.bot.aio.cursor.fetchall()) > 0:
                        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (mem.id, ))
                        currentDaily = int((await self.bot.aio.cursor.fetchall())[0][1])
                    else :
                        currentDaily = 0

                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
                    level = (await self.bot.aio.cursor.fetchall())[0][4]

                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
                    note = (await self.bot.aio.cursor.fetchall())[0][5]

                    back = Image.open("exts/Images/background.png")
                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id, ))
                    current_banner = (await self.bot.aio.cursor.fetchall())[0][2]
                    background = Image.open(f"exts/Images/{current_banner}.jpg")
                    background = background.resize((500, 215))
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
            await self.bot.aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (mem.id, 0, 'banner-9', 'None', 1, 'I am imperfectly perfect...', 0, "banner-9"))
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


    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command() 
    async def top(self, ctx):
        msg = await ctx.send("***Wait until i gather all the users...***") 
        await self.bot.aio.execute("SELECT * FROM profile")
        rowcount = len(await self.bot.aio.cursor.fetchall())
        ems = []
        counter, rank = 0, 0
        async with ctx.typing():
            for n in range(10, rowcount, 10):
                await self.bot.aio.execute("SELECT id, xp FROM profile ORDER BY xp DESC LIMIT %s OFFSET %s", (n, n-10))
                em = discord.Embed(title = "Top", description = "```\n", color = 0x00FFFF)
                for i in await self.bot.aio.cursor.fetchall():
                    counter += 1
                    if i[0] == ctx.author.id: 
                        rank = counter
                    mem = await self.bot.get_user_info(i[0])
                    data = (mem.name, str(i[1])) 
                    em.description += f"{data [0]:<20} : {data[1]}\n"
                em.description += "```"
                ems.append(em)
        info_embed = discord.Embed(title = "Help Info", description = "\u23EA:  Go to the first page\n\u25C0:  Go to the previous page\n\u23F9:  Stop the help command\n\u25B6:  Go to the next page\n\u23E9:  Go to the last page\n\U0001f522:  Asks for a page number\n\u2139:  Shows this info", colour = 0x00FFFF)
        for e in ems: 
            e.add_field(name = "Your guild rank", value = str(rank))
        ems.append (info_embed)
        await msg.edit(embed = ems[0])
        pa = Paginator(self.bot, msg, ctx.author, 0)
        await pa.paginate(ems)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def banner(self, ctx, option = "show", arg = None):
        '''Sets, shows, buys. or lists banners'''
        with open('exts/HelperFiles/banner_list.json') as fp:
            banners = json.load(fp)
        
        await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))

        if len(await self.bot.aio.cursor.fetchall()) > 0: #found in db
            if option == "show":
                await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))
                current_banner = (await self.bot.aio.cursor.fetchall())[0][2]
                em = discord.Embed(title = "Your current profile banner is: ", color = 0x00FFFF).set_image(url = banners[current_banner])
                await ctx.send(embed = em)

            elif option == "buy":
                if arg is None:
                    await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.author.id, ))
                    currentCredits = int((await self.bot.aio.cursor.fetchall())[0][1])
                    msg = await ctx.send("**Making the deck ready...**")
                    ems = []
                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))
                    purchased_banners = ((await self.bot.aio.cursor.fetchall())[0][-1]).split() #last column is banners purchased, is a string
                    
                    for i in banners:
                        if not i in purchased_banners:
                            em = discord.Embed(title = i, color = 0x00FFFF).set_image(url = banners[i])
                            em.add_field(name = "Price", value = "1000/- Rupees")
                            ems.append(em)
                    await msg.edit(embed = ems[0])
                    info_embed = discord.Embed(title = "Help Info", description = "\u23EA:  Go to the first page\n\u25C0:  Go to the previous page\n\u23F9:  Stop the help command\n\u25B6:  Go to the next page\n\u23E9:  Go to the last page\n\U0001f522:  Asks for a page number\n\u2139:  Shows this info", colour = 0x00FFFF)
                    ems.append(info_embed)
                    pa = Paginator(self.bot, msg, ctx.author, 0)
                    await pa.paginate(ems) 
                    if pa.item_purchased == True:
                        item = "banner-" + str(pa.index + 1)
                        await ctx.send("**You are about to buy {} for ₹1000/-.**\nType 'confirm' to confirm the purchase or 'cancel' to cancel it.".format(item))
                        def check(m):
                            return m.author.id == ctx.author.id and m.channel == ctx.channel
                        try:
                            response = await self.bot.wait_for('message', timeout = 20, check = check)
                            if response.content == "confirm":
                                if currentCredits < 1000:
                                    return await ctx.send("You don't have enough money to buy a banner.")
                                else:
                                    purchased_banners.append(item)
                                    await self.bot.aio.execute("UPDATE profile SET banners_buyed = %s WHERE id = %s", (' '.join(purchased_banners), ctx.author.id))
                                    await self.bot.aio.execute("UPDATE Dailies SET dailiesCount = %s WHERE id = %s", (currentCredits - 1000, ctx.author.id))
                                    await ctx.send("You successfully buyed {}.\nSay `iu banner set <banner name> to set the respective banner.".format(item))
                            else:
                                await ctx.send("Your purchase is cancelled.")
                        except asyncio.TimeoutError:
                            await ctx.send("No response from user. Purchase cancelled.")
                    else:
                        await ctx.send("Purchase cancelled.")
                elif arg not in banners:
                    await ctx.send("No such banner found.")
                else:
                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))
                    purchased_banners = ((await self.bot.aio.cursor.fetchall())[0][-1]).split() #last column is banners purchased, is a string
                    if arg in purchased_banners:
                        return await ctx.send("You have already purchased this item.")
                    else:
                        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.author.id, ))
                        currentCredits = int((await self.bot.aio.cursor.fetchall())[0][1])
                    
                        item = arg
                        await ctx.send("**You are about to buy {} for ₹1000/-.**\nType 'confirm' to confirm the purchase or 'cancel' to cancel it.".format(item))
                        def check(m):
                            return m.author.id == ctx.author.id and m.channel == ctx.channel
                        try:
                            response = await self.bot.wait_for('message', timeout = 20, check = check)
                            if response.content == "confirm":
                                if currentCredits < 1000:
                                    return await ctx.send("You don't have enough money to buy a banner.")
                                else:
                                    purchased_banners.append(item)
                                    await self.bot.aio.execute("UPDATE profile SET banners_buyed = %s", (' '.join(purchased_banners)))
                                    await self.bot.aio.execute("UPDATE Dailies SET dailiesCount = %s", (currentCredits - 1000, ))
                                    await ctx.send("You successfully buyed {}.\nSay `iu banner set <banner name> to set the respective banner.".format(item))
                            else:
                                await ctx.send("Your purchase is cancelled.")
                        except asyncio.TimeoutError:
                            await ctx.send("No response from user. Purchase cancelled.")

            elif option == "list":
                await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))
                purchased_banners = ((await self.bot.aio.cursor.fetchall())[0][-1]).split() #last column is banners purchased, is a string
                await ctx.send("Banners that you own are: `{}`".format(', '.join(purchased_banners)))
            elif option == "set":
                if arg is None:
                    await ctx.send("Please give the name of banner you want to set.")
                elif arg not in banners:
                    await ctx.send("No such banner found.")
                else:
                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))
                    purchased_banners = ((await self.bot.aio.cursor.fetchall())[0][-1]).split() #last column is banners purchased, is a string
                    if arg not in purchased_banners:
                        await ctx.send("You don't own this banner. To purchase it, type `IU banner buy {}`.".format(arg))
                    else:
                        await self.bot.aio.execute("UPDATE profile SET profile_background = %s", (arg, ))
                        await ctx.send("Your profile background has been set to {}.".format(arg))
                                    

        else: #not found in db
            #if person is not in db, insert a row with data and invoke the command again with respective arguments.
            await self.bot.aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ctx.author.id, 0, 'banner-9', 'None', 1, 'I am imperfectly perfect...', 0, "banner-9"))
            await ctx.invoke(self.bot.get_command("bannner"), option, arg)

def setup(bot):
    bot.add_cog(Profile(bot))
