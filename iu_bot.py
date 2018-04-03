import asyncio, datetime, functools, inspect, math, random, re, time

import aiohttp

import discord
from discord.ext import commands

# import bs4
# from bs4 import BeautifulSoup as bs

import globals

bot = commands.Bot(description='The offical bot overwatching Indians United.', command_prefix='iu_')

def tdm(td):
    return ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)

class Admin:
    '''for administrative purposes'''
    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        '''Kick members from your server'''
        try:
            await member.kick()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        '''Ban toxic members from your server'''
        try:
            await member.ban()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command(aliases=['cr', 'updaterole'])
    async def changerole(self, ctx, member: discord.Member, *, rolename):
        '''to add/remove a role from a person'''
        try:
            role = discord.utils.get(ctx.guild.roles, name=rolename)
            if role not in member.roles:
                await ctx.author.add_roles(role)
            else:
                await ctx.author.remove_roles(role)
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command()
    async def purge(self, ctx, number):
        '''clears specified number of messages, ranging from 2 to 100'''
        await ctx.channel.purge(limit=number)


class General:
    '''general commands'''
    @commands.command()
    async def ping(self, ctx):
        '''Call the bot'''
        msg = await ctx.send(ctx.author.mention+', Pong!')
        res = msg.created_at - ctx.message.created_at
        res = tdm(res)
        await msg.edit(content=ctx.author.mention+', Pong! :ping_pong: Took {} ms'.format(res))

    @commands.command()
    async def say(self, ctx, *, something='IU Bot Bot here!'):
        '''The bot becomes your copycat'''
        await ctx.send(something)
        await ctx.message.delete()

    @commands.command()
    async def now(self, ctx):
        '''Get current date and time'''
        m = str(datetime.datetime.now()).split()
        embed = discord.Embed(title='Date-time information',
                              color=eval(hex(ctx.author.color.value)))
        embed.add_field(name='Date', value='{}'.format(m[0]))
        embed.add_field(name='Time', value='{}GMT'.format(m[1]))
        await ctx.send(embed=embed)
        
    @commands.command(name = '8ball')
    async def _func(self, ctx, *, question):
        if question[-1] == '?':
            return await ctx.send(random.choice(globals.ballAnswers))
        await ctx.send('`Try again with a question!`')
        


@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name is globals.welcomeName:
            await bot.send_message(channel, 'Welcome to IU United, '+member.mention+'! Please enjoy your time here and hope you check #rules! :)')

@bot.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name is globals.leaveName:
            await ctx.send_message(channel, 'We are feeling bad to see you leaving %s!' %(member.name))

@bot.event
async def on_message(ctx):
    if ctx.channel.name is globals.memesChannel:
        for chr in list(string.ascii_letters):
            if chr in str(ctx.content):
                await ctx.delete_message(ctx)
    await bot.process_commands(ctx)

@bot.event
async def on_ready():
    # Added for testing purpose
    print('Ready!')

    bot.add_cog(General())
    bot.add_cog(Admin())

bot.run(globals.TOKEN)
