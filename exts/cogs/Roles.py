from discord.ext import commands
import discord

class Roles(commands.Cog):
    '''Self assignable roles'''
    def __init__(self,bot):
        self.bot=bot

    @commands.group(aliases=['roleme'], invoke_without_command=True)
    async def sar(self,ctx,*,role_name:str):
        roles=[ 'Sololearn', 'PUBG', 'Debater']
        if role_name.lower() not in [i.lower() for i in roles]:
            await ctx.send(":x: Error occured.Run `iu sar list` to see list of self assignable roles")
            return
        for role in roles:
            if role.lower() == role_name.lower():
                r=discord.utils.get(ctx.guild.roles,name=role)
                if r not in ctx.author.roles:
                    await ctx.author.add_roles(r)
                    await ctx.send(f"{ctx.author.name},{r.name} role added.Run this command again to remove this role")
                    return
                else:
                    await ctx.author.remove_roles(r)
                    await ctx.send(f"{ctx.author.name},{r.name} role removed.Run this command again to add this role")
                    return
    @sar.command(name='list')
    async def sar_list(self,ctx):
        roles=enumerate([ 'Sololearn', 'PUBG', 'Debater'],1)
        string=''
        for count,value in roles:
            string+=f'{count}) {value} \n'
        await ctx.send("Self Assignable Roles: \n"+ string +"type `iu roleme <role name>` to get or get rid of roles.")

def setup(bot):
    bot.add_cog(Roles(bot))
