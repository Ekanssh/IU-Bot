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
    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member,*,reason):
        '''Kick members from your server'''
        try:
            await member.kick(reason=reason)
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member,*,reason):
        '''Ban toxic members from your server'''
        try:
            await member.ban(reason=reason)
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(aliases=['cr', 'updaterole'],hidden=True)
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

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def warn(ctx, user:discord.Member, *, reason):
        '''warns an offender'''
        try:
            warn_embed=discord.Embed(title="You've been warned in Indians United",colour=discord.Colour.red())
            warn_embed.description=f"You've been warned for the following reason: {reason}")
            await user.send(embed=warn_embed)
            await ctx.send(f"Alright! {user.name} has been warned by {ctx.author.name} ")
        except Exception as e:
            await ctx.send(f"{e}")

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        '''Clears specified number of messages'''
        while number != 0:
            if number<=99:
                await ctx.channel.purge(limit=number+1)
            else:
                await ctx.channel.purge(limit=100)
                number-=100


def setup(bot):
    bot.add_cog(Admin(bot))
