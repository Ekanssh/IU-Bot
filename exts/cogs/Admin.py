#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio, aiohttp #various needs


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
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        '''Clears specified number of messages, ranging from 2 to 100'''
        await ctx.channel.purge(limit=number)


def setup(bot):
    bot.add_cog(Admin(bot))