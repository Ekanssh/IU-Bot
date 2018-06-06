from discord.ext import commands
import discord

class Economy:
    '''Economy commands like dailies, credits, level'''

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def level(self, ctx, person: discord.Member=None):

        '''get your XP and level stats'''

        person = person or ctx.author

        searchable = person.id
        await bot.aio.execute("SELECT * FROM profile WHERE id = %s", (searchable, ))

        temp = (await bot.aio.cursor.fetchall())[0]

        level, xp = temp[4], temp[6]
        if xp < 1000:
            embed = discord.Embed(title = person.name + "'s level",
                                    description = "Level "+ str(level) + "\n" + str(xp) + " xp",
                                    colour = discord.Colour.from_rgb(205, 127, 50))
        elif xp < 5000:
            embed = discord.Embed(title = person.name+"'s level",
                                    description="Level " + str(level) + "\n" + str(xp) + " xp",
                                    colour = discord.Colour.from_rgb(218, 218, 218))
        elif xp < 10000:
            embed = discord.Embed(title = person.name + "'s level", 
                                    description = "Level " + str(level) + "\n" + str(xp) + " xp",
                                    colour=discord.Colour.gold())
        else: 
            embed = discord.Embed(title = person.name + "'s level",
                                    description = "Level " + str(level) + "\n" + str(xp) + " xp",
                                    colour = discord.Colour.from_rgb(20, 30, 179))
        await ctx.send(embed=embed)


    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    @commands.command(aliases=['daily'])
    async def dailies(self, ctx):
        '''Get your free ₹200'''
        if ctx.message.author.bot:
            await ctx.send("Sorry, bots have nothing to do with money")
            return
        msg_timestamp = ctx.message.created_at
        found = False
        await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id, ))

        for i in await bot.aio.cursor.fetchall():
            if i is not None:
                found = True
                await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id, ))
                previous_msg_timestamp = (await bot.aio.cursor.fetchall())[0][2]

                remaining_timestamp = previous_msg_timestamp - msg_timestamp

                await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id, ))
                currentDaily = int((await bot.aio.cursor.fetchall())[0][1])

                secondsRemaining = abs(remaining_timestamp.seconds)
                time = str(datetime.timedelta(seconds = secondsRemaining)).split(":")

                if secondsRemaining >= 43200:
                    currentDaily += 200
                    await bot.aio.execute("UPDATE Dailies SET dailiesCount = %s, remaining_timestamp = %s WHERE id = %s", (currentDaily, msg_timestamp, ctx.message.author.id, ))
                    await ctx.send(":moneybag: | You got your 200 dialies!\n You have ₹{}".format(currentDaily))

                else:
                    await ctx.send("Sorry, you can claim your dailies in {0}hrs, {1}mins, {2}s\nYou have ₹{3}:moneybag:".format(time[0], time[1], time[2], currentDaily))

        if not found:
            await ctx.send("Member not found in the database. Registering new user with id {0}".format(ctx.author.id))
            await bot.aio.execute("INSERT INTO Dailies VALUES (%s, '200', %s)", (ctx.message.author.id, msg_timestamp, ))
            await ctx.send(":moneybag: | You got your 200 dialies!\nYou have ₹200")



    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def credits(self, ctx, otherMem: discord.Member = None):
        '''Check your or someone else's credits'''
        if ctx.message.author.bot or (otherMem is not None and otherMem.bot):
            await ctx.send("Sorry, bot have nothing to do with money")
            return
        found_in_db = False
        if otherMem is None:
            await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id,))
            for i in await bot.aio.cursor.fetchall():
                if i is not None:
                    if i[0] == ctx.message.author.id:
                        found_in_db = True
                        await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (ctx.message.author.id,))
                        await ctx.send(":moneybag: | You currently have ₹{0}".format((await bot.aio.cursor.fetchall())[0][1]))
            if not found_in_db:
                await ctx.send(":moneybag: | You currently have ₹0")
        else:
            await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (otherMem.id,))
            for i in await bot.aio.cursor.fetchall():
                if i is not None:
                    if i[0] == otherMem.id:
                        found_in_db = True
                        await bot.aio.execute("SELECT * FROM Dailies WHERE id = %s", (otherMem.id,))
                        await ctx.send(":moneybag: | {0} currently has ₹{1}".format(otherMem.name, (await bot.aio.cursor.fetchall())[0][1]))
            if not found_in_db:
                await ctx.send(":moneybag: | {0} currently has ₹0".format(otherMem.name))

def setup(bot):
    bot.add_cog(Economy(bot))