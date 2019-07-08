#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import aiohttp  # various needs
import json

class Admin(commands.Cog):
    '''For administrative purposes'''

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member,*,reason=None):
        '''Kick members from your server'''
        try:
            await member.kick(reason=reason)
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member,*,reason=None):
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
    async def warn(self,ctx, offender:discord.Member, *, reason):
        '''warns an offender'''
        try:
            warn_embed=discord.Embed(title=f"You've been warned in {ctx.guild}",colour=discord.Colour.red())
            warn_embed.description=f"You've been warned for the following reason: {reason}"
            await offender.send(embed=warn_embed)
            await ctx.send(f"Alright! {offender.name} has been warned by {ctx.author.name} ")
        except Exception as e:
            await ctx.send(f"{e}")

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int, author: discord.Member = None):
        '''Clears specified number of messages'''
        if author is not None:
            check = lambda x: x.author == author
            deleted=await ctx.channel.purge(limit=number + 1, check=check)
            await ctx.send("Purged %d messages from %s" % (number, author), delete_after=3)
        else:
            deleted=await ctx.channel.purge(limit=number + 1)
            await ctx.send("Purged %d messages in this channel" % number, delete_after=3)
        messages=''
        for msg in deleted:
            messages+=f'{msg.author} on {msg.created_at} :: {msg.content or "Attachment/Embed"}\n'
        link=await self.haste_post(messages)
        result=f"""{ctx.author} cleared {len(deleted)} messages in {ctx.channel.mention}
        Here is the list of messages cleared
        {link}"""
        await self.bot.get_channel(450997458600984586).send(result)

    async def haste_post(self, content):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://paste.pydis.com/documents",data=content.encode('utf-8')) as post:
                data=await post.read()
                jsondata=json.loads(data)
                return "https://paste.pydis.com/{}".format(jsondata['key'])


def setup(bot):
    bot.add_cog(Admin(bot))
