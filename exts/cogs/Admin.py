#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import aiohttp  # various needs


class Admin:
    '''For administrative purposes'''

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        '''Kick members from your server'''
        try:
            await member.kick()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        '''Ban toxic members from your server'''
        try:
            await member.ban()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(aliases=['cr', 'updaterole'])
    @commands.has_permissions(manage_roles=True)
    async def changerole(self, ctx, member: discord.Member, *, rolename):
        '''To add/remove a role from a person'''
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
    async def warn(ctx, user:discord.Member, *, reason):
        '''Warns an offender'''
        try:
            warn_embed=discord.Embed(title="You've been warned in Indians United",colour=discord.Colour.red())
            if ctx.author.top_role.name in ["Queens","Lords","Nobles"]:
                warn_embed.description="You've been warned by {} for the following reason: {}".format(ctx.author.name,reason)
                await user.send(embed=warn_embed)
            else:
                warn_embed.description="You've been warned for trying to warn a user without the permissions."
                await ctx.author.send(embed=warn_embed)
        except Exception as e:
            await ctx.send(f"{e}")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        '''Clears specified number of messages, ranging from 2 to 100'''
        await ctx.channel.purge(limit=number)


def setup(bot):
    bot.add_cog(Admin(bot))
