from discord.ext import commands
import discord
import datetime
import re
import asyncio
import random


class Economy:
    '''Economy commands like dailies, credits, level'''

    def __init__(self, bot):
        self.bot = bot

    async def special_user_fetcher(self,ctx,user):
        try:
            if user is None:
                return ctx.message.author
            elif len(ctx.message.mentions)>0:
                return ctx.message.mentions[0]
            else:
                results = []
                for i in ctx.message.guild.members:
                    if user.lower() in i.name.lower() or user==str(i) or user.lower() in i.display_name.lower() or user in str(i.id):
                        results.append(i)
                if len(results)>0:
                    if len(results)==1:
                        return results[0]
                    else:
                        stri=""
                        counter=1
                        await ctx.send("Multiple members found. Please choose one of the following, or type cancel.")
                        for i in results:
                            stri+=str(counter)+". "+"``"+str(i)+"``"+"\n"
                            counter+=1
                        await ctx.send(stri)
                        def check(p):
                            return p.author.id == ctx.author.id and p.channel == ctx.channel
                        m =await self.bot.wait_for('message', check = check)
                        def check2(p):
                            return p.author.id in [ctx.author.id,self.bot.user.id] and p.channel == ctx.channel
                        if m.content.lower()=="cancel":
                            await ctx.channel.purge(limit=4,check=check2)
                            await ctx.send(":x: Command Cancelled.")
                            return "cancel"
                        else:
                            await ctx.channel.purge(limit=4,check=check2)
                            m=int(m.content)-1
                            return results[m]
                else:
                    return None
        except Exception as e:
            print(e)
            return None


    @commands.command()
    async def level(self, ctx, person=None):

        '''Get your XP and level stats'''
        person=await self.special_user_fetcher(ctx,person)
        if person=="cancel":
            return
        if person is None:
            await ctx.send("Dear {},the user you typed does not seem to exist. Please make sure you provided correct details.".format(ctx.message.author.mention))
            return
        if person.bot==True:
            await ctx.send("Bots do not have levels")
            return
        searchable = person.id
        await self.bot.aio.execute("SELECT * FROM profile WHERE id = %s", (searchable, ))

        temp = (await self.bot.aio.cursor.fetchall())[0]

        level, xp = temp[4], temp[6]
        if xp < 1000:
            embed = discord.Embed(title=person.name + "'s level",
                                  description="Level " +
                                  str(level) + "\n" + str(xp) + " xp",
                                  colour=discord.Colour.from_rgb(205, 127, 50))
        elif xp < 5000:
            embed = discord.Embed(title=person.name+"'s level",
                                  description="Level " +
                                  str(level) + "\n" + str(xp) + " xp",
                                  colour=discord.Colour.from_rgb(218, 218, 218))
        elif xp < 10000:
            embed = discord.Embed(title=person.name + "'s level",
                                  description="Level " +
                                  str(level) + "\n" + str(xp) + " xp",
                                  colour=discord.Colour.gold())
        else:
            embed = discord.Embed(title=person.name + "'s level",
                                  description="Level " +
                                  str(level) + "\n" + str(xp) + " xp",
                                  colour=discord.Colour.from_rgb(20, 30, 179))
        await ctx.send(embed=embed)

    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    @commands.command(aliases=['daily'])
    async def dailies(self, ctx):
        '''Get your free ₹200 in every 12hrs'''
        if ctx.message.author.bot:
            await ctx.send("Sorry, bots have nothing to do with money")
            return
        msg_timestamp = ctx.message.created_at
        found = False
        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id, ))
        customer_data = await self.bot.aio.cursor.fetchone()
        if customer_data is not None:
            found = True
            previous_msg_timestamp = customer_data[2]
            difference_timestamp = (msg_timestamp - previous_msg_timestamp)
            last_payed_ago = abs(difference_timestamp.total_seconds())
            currentDaily = customer_data[1]
            if last_payed_ago >= 43200:
                currentDaily += 200
                await self.bot.aio.execute("UPDATE Dailies SET dailiesCount = %s, remaining_timestamp = %s WHERE id = %s", (currentDaily, msg_timestamp, ctx.message.author.id, ))
                await ctx.send(":moneybag: | You got your 200 dailies!\n You have ₹{}".format(currentDaily))
            else:
                secondsRemaining = 43200 - abs(difference_timestamp.seconds)
                time = str(datetime.timedelta(
                    seconds=secondsRemaining)).split(":")
                await ctx.send("Sorry, you can claim your dailies in {0}hrs, {1}mins, {2}s\nYou have ₹{3}:moneybag:".format(time[0], time[1], time[2], currentDaily))
        if not found:
            await self.bot.aio.execute("INSERT INTO Dailies VALUES (%s, %s, %s)", (ctx.message.author.id, 200, msg_timestamp))
            await ctx.send(":moneybag: | You got your 200 dailies!\nYou have ₹200")

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def credits(self, ctx, otherMem= None):
        '''Check your or someone else's credits'''
        otherMem=await self.special_user_fetcher(ctx,otherMem)
        if otherMem=="cancel":
            return
        if otherMem is None:
            await ctx.send("Dear {},the user you typed does not seem to exist. Please make sure you provided correct details.".format(ctx.message.author.mention))
            return
        if otherMem.bot==True:
            await ctx.send("Sorry, bot have nothing to do with money")
            return
        found_in_db = False
        if otherMem is None:
            await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id,))
            for i in await self.bot.aio.cursor.fetchall():
                if i is not None:
                    if i[0] == ctx.message.author.id:
                        found_in_db = True
                        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id,))
                        await ctx.send(":moneybag: | You currently have ₹{0}".format((await self.bot.aio.cursor.fetchall())[0][1]))
            if not found_in_db:
                await ctx.send(":moneybag: | You currently have ₹0")
        else:
            await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (otherMem.id,))
            for i in await self.bot.aio.cursor.fetchall():
                if i is not None:
                    if i[0] == otherMem.id:
                        found_in_db = True
                        await self.bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (otherMem.id,))
                        await ctx.send(":moneybag: | {0} currently has ₹{1}".format(otherMem.name, (await self.bot.aio.cursor.fetchall())[0][1]))
            if not found_in_db:
                await ctx.send(":moneybag: | {0} currently has ₹0".format(otherMem.name))

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def pay(self, ctx,amount: int,*, mem=None):
        mem=await self.special_user_fetcher(ctx,mem)
        if mem=="cancel":
            return
        if mem is None:
            await ctx.send("Dear {},the user you typed does not seem to exist. Please make sure you provided correct details.".format(ctx.message.author.mention))
            return
        if mem.bot==True:
            await ctx.send("Sorry, bot have nothing to do with money")
            return
        if ctx.author.id is mem.id:
            await ctx.send("Want to some Credits,try collecting your free dailies")
            return
        if amount <= 0:
            failure_embed=discord.Embed(title="Payment Cancelled",description='Enter a valid amount',color=discord.Colour.red())
            await ctx.send(embed=failure_embed)
        found_author = False
        found_mem = False
        author_bal = None
        mem_bal = None
        valid_emojis=['\U0001f1fe','\U0001f1f3']
        def check(reaction,user):
            return reaction.emoji in valid_emojis and user is ctx.author
        await self.bot.aio.execute("SELECT dailiesCount FROM Dailies WHERE id = %s", (ctx.message.author.id, ))
        author_bal = (await self.bot.aio.cursor.fetchone())
        if author_bal is not None:
            author_bal=author_bal[0]
            found_author = True
        await self.bot.aio.execute("SELECT dailiesCount FROM Dailies WHERE id = %s", (mem.id, ))
        mem_bal = (await self.bot.aio.cursor.fetchone())
        if mem_bal is not None:
            mem_bal=mem_bal[0]
            found_mem = True
        if found_author and found_mem:
            if author_bal >= amount:
                prompt=await ctx.send(f"""You are about to pay ₹{amount} to {mem.name}
                Press :regional_indicator_y: to CONFIRM
                Press :regional_indicator_n: to CANCEL """)
                await prompt.add_reaction("\U0001f1fe")
                await prompt.add_reaction("\U0001f1f3")
                try:
                    r,u=await self.bot.wait_for('reaction_add', timeout=20, check=check)
                    if r.emoji == valid_emojis[0]:
                        await self.bot.aio.execute('UPDATE Dailies SET dailiesCount=%s WHERE id=%s',(author_bal-amount,ctx.author.id,))
                        await self.bot.aio.execute('UPDATE Dailies SET dailiesCount=%s WHERE id=%s',(mem_bal+amount,mem.id,))
                        acknowledgement_embed=discord.Embed(title="Payment Successfull")
                        acknowledgement_embed.description=f"₹{amount} added to {mem.mention}"
                        acknowledgement_embed.color=discord.Colour.green()
                        await prompt.clear_reactions()
                        await prompt.edit(content='',embed=acknowledgement_embed)
                    elif r.emoji == valid_emojis[1]:
                        failure_embed=discord.Embed(title="Payment Cancelled",description='Cancelled by Payee',color=discord.Colour.red())
                        await prompt.clear_reactions()
                        await prompt.edit(content='',embed=failure_embed)
                except asyncio.TimeoutError:
                    failure_embed=discord.Embed(title="Payment Cancelled",description='Session Expired',color=discord.Colour.red())
                    await prompt.clear_reactions()
                    await prompt.edit(content='',embed=failure_embed)
            else:
                failure_embed=discord.Embed(title="Payment Cancelled",description='Insufficient Credits',color=discord.Colour.red())
                await ctx.send(embed=failure_embed)
        elif found_author and not found_mem:
            failure_embed=discord.Embed(title="Payment Unsuccessfull",color=discord.Colour.red())
            failure_embed.description=f"Receiver Account not Found\nAsk {mem.name} to collect dailies to open account and try again"
            await ctx.send(embed=failure_embed)
        elif not found_author and found_mem:
            failure_embed=discord.Embed(title="Payment Unsuccessfull",color=discord.Colour.red())
            failure_embed.description=f"Payee Account not Found\nGo get yours by collecting daily credits now!"
            await ctx.send(embed=failure_embed)
        else:
            failure_embed=discord.Embed(title="Payment Unsuccessfull",color=discord.Colour.red())
            failure_embed.description=f"Accounts does not exist\nStart collecting your free dailies now!"
            await ctx.send(embed=failure_embed)


def setup(bot):
    bot.add_cog(Economy(bot))
