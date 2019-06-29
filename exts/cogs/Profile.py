#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from exts.cogs.Paginator import Paginator
from PIL import Image, ImageFont, ImageDraw  # used in profile command
import aiohttp
import os
import json
import asyncio
import datetime


class Profile(commands.Cog):
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
                    else:
                        currentDaily = 0
                    await self.bot.aio.execute("SELECT reps from rep where id= %s", (mem.id, ))
                    rep_data = await self.bot.aio.cursor.fetchone()
                    reps = 0
                    if rep_data is not None:
                        reps = rep_data[0]

                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
                    level = (await self.bot.aio.cursor.fetchall())[0][4]

                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
                    note = (await self.bot.aio.cursor.fetchall())[0][5]

                    back = Image.open("exts/Images/background.png")
                    await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id, ))
                    current_banner = (await self.bot.aio.cursor.fetchall())[0][2]
                    background = Image.open(
                        f"exts/Images/{current_banner}.jpg")
                    background = background.resize((500, 215))
                    back.paste(background, box=(0, 0))
                    font = ImageFont.truetype(
                        "exts/Fonts/Quicksand-Regular.otf", 45)
                    badges_font = ImageFont.truetype(
                        "exts/Fonts/Quicksand-Regular.otf", 25)
                    level_font = ImageFont.truetype(
                        "exts/Fonts/Quicksand-Regular.otf", 25)
                    credits_reps_font = ImageFont.truetype(
                        "exts/Fonts/Quicksand-Regular.otf", 20)
                    note_font = ImageFont.truetype(
                        "exts/Fonts/Quicksand-Regular.otf", 20)

                    d = ImageDraw.Draw(back)
                    d.rectangle([0, 160, 110, 270], fill=(255, 255, 255))
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(str(mem.avatar_url)) as r:
                            with open("TEMPava.png", 'wb') as ava:
                                ava.write(await r.read())
                    avatar = Image.open("TEMPava.png")
                    avatar = avatar.resize((100, 100))
                    back.paste(avatar, (5, 165))
                    d.text(text=str(mem.name), xy=(125, 215), font=font)
                    d.line([(113, 219), (113, 500)], fill=(
                        50, 50, 50), width=3)  # line beside ava

                    d.line([(11, 302), (100, 302)], fill=(50, 50, 50), width=3)
                    d.text(text="Badges", xy=(10, 275), font=badges_font)
                    d.text(text="Level:", xy=(360, 265), font=level_font)
                    d.text(text=str(level), xy=(435, 265), font=level_font)

                    d.text(text="Credits:", xy=(135, 310),
                           font=credits_reps_font)
                    d.text(text=str(currentDaily), xy=(435, 310),
                           font=credits_reps_font, align='RIGHT')

                    d.text(text="Reputations:", xy=(
                        135, 340), font=credits_reps_font)
                    d.text(text=str(reps), xy=(435, 340),
                           font=credits_reps_font, align='RIGHT')

                    d.rectangle([135, 400, 480, 490])
                    d.text(text=note, xy=(145, 405), font=note_font)
                    back.save(str(mem.name) + '.png')
                    await ctx.send(file=discord.File(str(mem.name) + '.png'))
                    os.remove(str(mem.name) + '.png')
                    os.remove('TEMPava.png')

        if not found:
            await self.bot.aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (mem.id, 0, 'banner-9', 'None', 1, 'I am imperfectly perfect...', 0, "banner-9"))
            await ctx.invoke(self.bot.get_command("profile"), mem)

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def note(self, ctx, option="show", *, newNote=None):
        '''Set your profile's note'''
        if ctx.message.author.bot:
            return
        if option == "show":
            await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.message.author.id,))
            note = (await self.bot.aio.cursor.fetchall())[0][5]
            await ctx.send("Your current note is:\n" + "```" + note + "```")
        elif option == "set" and newNote is not None:
            await self.bot.aio.execute("UPDATE profile SET note = %s WHERE id = %s", (newNote, ctx.message.author.id, ))
            await ctx.send("Your current note is:\n" + "```" + newNote + "```")
        elif option == "reset":
            await self.bot.aio.execute("UPDATE profile SET note = %s WHERE id = %s", ('I am imperfectly perfect...', ctx.message.author.id, ))
            await ctx.send("Your profile's note has been reset to:\n" + '```I am imperfectly perfect...```')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def rep(self, ctx, *, mem: discord.Member):
        '''Give a reputation point to persons u like'''
        msg_ts = ctx.message.created_at
        if ctx.author.bot or mem.bot:
            await ctx.send("Sorry!, Humans Only")
            return
        if ctx.author.id is mem.id:
            await ctx.send("You can not give reputation point to yourself.")
            return

        found_author = False
        found_mem = False
        last_given_ts = None
        difference_ts = None
        repFlag = False
        currentRep = 0

        # fetching author and member
        await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (ctx.message.author.id, ))
        author_data = await self.bot.aio.cursor.fetchone()
        if author_data is not None:
            found_author = True
            last_given_ts = author_data[2]
            if last_given_ts is not None:
                difference_ts = msg_ts-last_given_ts
                repFlag = (abs(difference_ts.total_seconds()) >= 18000)
            else:
                repFlag = True
        await self.bot.aio.execute("SELECT * FROM rep WHERE id = %s", (mem.id, ))
        mem_data = await self.bot.aio.cursor.fetchone()
        if mem_data is not None:
            found_mem = True
            currentRep = mem_data[1]

        # now comes function
        if found_author and found_mem:
            if repFlag:
                await self.bot.aio.execute("UPDATE rep SET reps = %s WHERE id = %s", (currentRep + 1, mem.id, ))
                await self.bot.aio.execute("UPDATE rep SET last_given = %s WHERE id = %s", (msg_ts, ctx.author.id, ))
                await ctx.send("You have given reputation point to " + mem.mention)
            else:
                remaining_seconds = 18000 - abs(difference_ts.seconds)
                time = str(datetime.timedelta(
                    seconds=remaining_seconds)).split(":")
                await ctx.send("Sorry, you can award more reputation in {0}hrs, {1}mins".format(time[0], time[1]))

        elif found_author and not found_mem:
            if repFlag:
                await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 1, %s)", (mem.id, None,))
                await self.bot.aio.execute("UPDATE rep SET last_given = %s WHERE id = %s", (msg_ts, ctx.author.id, ))
                await ctx.send("You have given reputation point to " + mem.mention)
            else:
                remaining_seconds = 18000 - abs(difference_ts.seconds)
                time = str(datetime.timedelta(
                    seconds=remaining_seconds)).split(":")
                await ctx.send("Sorry, you can award more reputation in {0}hrs, {1}mins".format(time[0], time[1]))

        elif found_mem and not found_author:
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 0, %s)", (ctx.author.id, msg_ts,))
            await self.bot.aio.execute("UPDATE rep SET reps = %s WHERE id = %s", (currentRep + 1, mem.id, ))
            await ctx.send("You have given reputation point to " + mem.mention)
        else:
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 0, %s)", (ctx.message.author.id, msg_ts,))
            await self.bot.aio.execute("INSERT INTO rep VALUES (%s, 1, %s)", (mem.id, None,))
            await ctx.send("You have given reputation point to " + mem.mention)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command()
    async def top(self, ctx):
        '''Check IU Leaderboards to see ur rank or other's'''
        msg = await ctx.send("***Wait until i gather all the users...***")
        await self.bot.aio.execute("SELECT id, xp FROM profile")
        l = await self.bot.aio.cursor.fetchall()
        rowcount = len(l)
        ems = []
        counter, rank = 1, 0
        async with ctx.typing():
            l.sort(key = lambda el: el[1], reverse = True)
            for n in range(10, rowcount, 10):
                em = discord.Embed(title="Top", description="```\n", color=0x00FFFF)
                t = l[n-10: n]
                showable = []
                for i in t:
                    if i[0] == ctx.author.id:
                        rank = counter
                    if i[0] in self.bot._memList:
                        data = (str(counter)+") "+self.bot._memList[i[0]] or "None", str(i[1]))
                    else:
                        data = (str(counter)+") "+str(i[0]), str(i[1]))
                    showable.append(data)
                    counter += 1
                length = max([len(i[0]) for i in showable])
                for i in showable:
                    em.description += f"{data[0]:<length} : {data[1]}\n"
                em.description += "```"
                ems.append(em)
        for e in ems:
            e.add_field(name=f"{ctx.author.name}, Your guild rank", value=str(rank))
        await msg.edit(embed=ems[0])
        pa = Paginator(self.bot, msg, ctx.author, 0)
        await pa.paginate(ems)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def banner(self, ctx, option="show", arg=None):
        '''Sets, shows, buys or lists banners'''
        with open('exts/HelperFiles/banner_list.json') as fp:
            banners = json.load(fp)

        await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.author.id, ))
        user_profile = await self.bot.aio.cursor.fetchall()

        if len(user_profile) > 0:  # found in db
            if option == "show":
                current_banner = user_profile[0][2]
                em = discord.Embed(title="Your current profile banner is: ", color=0x00FFFF).set_image(
                    url=banners[current_banner])
                await ctx.send(embed=em)

            elif option == "buy":
                if arg is None:
                    await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.author.id, ))
                    d = await self.bot.aio.cursor.fetchall()
                    currentCredits = int(d[0][1])
                    msg = await ctx.send("**Making the deck ready...**")
                    ems = []
                    # last column is banners purchased, is a string
                    purchased_banners = (user_profile[0][-1]).split()
                    for i in banners:
                        if not i in purchased_banners:
                            em = discord.Embed(title=i, color=0x00FFFF).set_image(url=banners[i])
                            em.add_field(name="Price", value="1000/- IUC")
                            ems.append(em)
                    await msg.edit(embed=ems[0])

                    pa = Paginator(self.bot, msg, ctx.author, 0)
                    await pa.paginate(ems)
                    if pa.item_purchased == True:
                        item = msg.embeds[0].title
                        await ctx.send("**You are about to buy {} for 1000/- IUC.**\nType 'CONFIRM' to confirm the purchase or 'cancel' to cancel it.".format(item))

                        def check(m):
                            return m.author.id == ctx.author.id and m.channel == ctx.channel
                        try:
                            response = await self.bot.wait_for('message', timeout=20, check=check)
                            if response.content == "CONFIRM":
                                if currentCredits < 1000:
                                    return await ctx.send("You don't have enough money to buy a banner.")
                                else:
                                    purchased_banners.append(item)
                                    await self.bot.aio.execute("UPDATE profile SET banners_buyed = %s WHERE id = %s", (' '.join(purchased_banners), ctx.author.id))
                                    await self.bot.aio.execute("UPDATE Dailies SET dailiesCount = %s WHERE id = %s", (currentCredits - 1000, ctx.author.id))
                                    await ctx.send("You successfully bought {}.\nType `iu banner set <banner name>` to set the respective banner.".format(item))
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
                    # last column is banners purchased, is a string
                    purchased_banners = ((await self.bot.aio.cursor.fetchall())[0][-1]).split()
                    if arg in purchased_banners:
                        return await ctx.send("You have already purchased this item.")
                    else:
                        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.author.id, ))
                        currentCredits = int((await self.bot.aio.cursor.fetchall())[0][1])

                        item = arg
                        await ctx.send("**You are about to buy {} for ₹1000/-.**\nType 'CONFIRM' to confirm the purchase or 'cancel' to cancel it.".format(item))

                        def check(m):
                            return m.author.id == ctx.author.id and m.channel == ctx.channel
                        try:
                            response = await self.bot.wait_for('message', timeout=20, check=check)
                            if response.content == "CONFIRM":
                                if currentCredits < 1000:
                                    return await ctx.send("You don't have enough money to buy a banner.")
                                else:
                                    purchased_banners.append(item)
                                    purchased_banners.sort(key = lambda t: int(t[7:]))
                                    await self.bot.aio.execute("UPDATE profile SET banners_buyed = %s WHERE id = %s", (' '.join(purchased_banners), ctx.author.id))
                                    await self.bot.aio.execute("UPDATE Dailies SET dailiesCount = %s WHERE id = %s", (currentCredits - 1000, ctx.author.id, ))
                                    await ctx.send("You successfully bought {}.\nSay `iu banner set <banner name>` to set the respective banner.".format(item), ctx.author.id)
                            else:
                                await ctx.send("Your purchase is cancelled.")
                        except asyncio.TimeoutError:
                            await ctx.send("No response from user. Purchase cancelled.")

            elif option == "list":
                # last column is banners purchased, is a string
                purchased_banners = user_profile[0][-1].split()
                await ctx.send("Banners that you own are: `{}`".format(', '.join(purchased_banners)))
            elif option == "set":
                if arg is None:
                    await ctx.send("Please give the name of banner you want to set.")
                elif arg not in banners:
                    await ctx.send("No such banner found.")
                else:
                    # last column is banners purchased, is a string
                    purchased_banners = user_profile[0][-1].split()
                    if arg not in purchased_banners:
                        await ctx.send("You don't own this banner. To purchase it, type `IU banner buy {}`.".format(arg))
                    else:
                        await self.bot.aio.execute("UPDATE profile SET profile_background = %s WHERE id = %s", (arg, ctx.author.id, ))
                        await ctx.send("Your profile background has been set to {}.".format(arg))

        else:  # not found in db
            # if person is not in db, insert a row with data and invoke the command again with respective arguments.
            await self.bot.aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ctx.author.id, 0, 'banner-9', 'None', 1, 'I am imperfectly perfect...', 0, "banner-9"))
            await ctx.invoke(self.bot.get_command("bannner"), option, arg)


def setup(bot):
    bot.add_cog(Profile(bot))
