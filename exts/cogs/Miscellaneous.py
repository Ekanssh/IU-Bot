#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord 


class Miscellaneous:
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fb'])
    async def feedback(self,ctx,*,message):
        '''Please provide any feedback and report any bugs.'''
        author = ctx.message.author.name + " said in " + "'" + ctx.guild.name + "'"
        await self.bot.get_guild(381052278708240385).get_channel(435375286385770497).send(embed=discord.Embed(color=eval(hex(ctx.author.color.value)),title=author,description="#"+ctx.channel.name+":\n"+message))
        await ctx.message.add_reaction('\u2705')
        
    @commands.command(aliases=["h"])
        async def help(self,ctx):
        '''bot help message'''
        command_list={}
        message={}
        embeds=[]
        for i in bot.cogs.keys():
                if i!='REPL':command_list.update({i:(m for m in dir(bot.get_cog(i))[26:])})
                else:command_list.update({'REPL':('exec','repl')})
        for i in bot.commands:
                f=inspect.getsource(bot.get_command(str(i)).callback)
                message.update({str(i):f.split("\n")[2].strip()[3:-3]})
        em=discord.Embed(title="IU Bot Help Message",color=eval(hex(ctx.author.color.value)))
        for i in command_list.keys():
                embeds.append(discord.Embed(title=i+" help",description="\n".join([m+": "+message[m] for m in command_list[i]]),inline=False,colour=ctx.author.colour))
        #till now we got the embeds, now for paginator
        info_embed=discord.Embed(title="IU Bot help message",description="""Please press:
        \u23EA to view the very first help message.
        \u25C0 to scroll backward
        \u23F9 to stop looking through the commands
        \u25B6 to scroll forward
        \u23E9 to view the very last help message
        \U0001f522 to search by page 
        \u2139 to view this help message""",colour=ctx.author.colour)
        curr=0
        reactions=['\u23EA','\u25C0','\u23F9','\u25B6','\u23E9','\U0001f522','\u2139']
        mess=await ctx.send(embed=info_embed)
        cogc=len(list(bot.cogs.keys()))-1
        for i in reactions:
            await mess.add_reaction(i)
        while True:
            try:
                waiting=await bot.wait_for('reaction_add',check=lambda reaction,user:(user.id==ctx.author.id) and (reaction.emoji in reactions),timeout=60)
                if waiting[0].emoji=="\u23EA":
                        curr=0
                        await mess.edit(embed=embeds[0])
                elif waiting[0].emoji=="\u25C0":
                        if curr==0:curr=cogc
                        else:curr-=1
                        await mess.edit(embed=embeds[curr])
                elif waiting[0].emoji=="\u23F9":
                        break
                elif waiting[0].emoji=="\u25B6":
                        if curr==cogc:curr=0
                        else:curr+=1
                        await mess.edit(embed=embeds[curr])
                elif waiting[0].emoji=="\u23E9":
                        curr=cogc
                        await mess.edit(embed=embeds[cogc])
                elif waiting[0].emoji=="\U0001f522":
                        await ctx.send("Select your page number (from 1 to %d)"%(cogc+1))
                        num=await bot.wait_for('message',check=lambda message:(message.content in [str(i+1) for i in range(cogc+1)]) and (message.author.id==ctx.author.id),timeout=60)
                        curr=int(num.content)-1
                        await mess.edit(embed=embeds[curr])
                elif waiting[0].emoji=="\u2139":
                        await mess.edit(embed=info_embed)
    	    except asyncio.TimeoutError:
                break
	await mess.edit(embed=discord.Embed(title="You have just used IU Bot's help message",description="Thank you!",colour=ctx.author.colour))

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
