from discord.ext import commands
import discord

class Roles(commands.Cog):
    '''Self assignable roles'''
    def __init__(self,bot):
        self.bot=bot

    @commands.group(aliases=['roleme'], invoke_without_command=True)
    async def sar(self,ctx,*,role_name:str):
        '''Self Assignable Roles'''
        await self.bot.aio.execute("SELECT * FROM sar")
        fetch= await self.bot.aio.cursor.fetchall()
        if len(fetch) == 0:
            await ctx.send("No self assignable roles configured")
            return
        roles=[]
        for role in fetch:
            roles.append(role[0])
        if role_name.lower() not in [i.lower() for i in roles]:
            await ctx.send(":x: Error occured. Run `iu sar list` to see list of self assignable roles")
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
        await self.bot.aio.execute("SELECT * FROM sar")
        fetch= await self.bot.aio.cursor.fetchall()
        if len(fetch) == 0:
            await ctx.send("No self assignable roles configured")
            return
        roles=[]
        for role in fetch:
            roles.append(role[0])
        roles=enumerate(roles,1)
        string=''
        for count,value in roles:
            string+=f'{count}) {value} \n'
        await ctx.send("Self Assignable Roles: \n"+ string +"type `iu roleme <role name>` to get or get rid of roles.")
    
    @sar.command(name= 'config', hidden=True)
    @commands.has_any_role('Lords', 'IU Bot Dev')
    async def _sar_add(self,ctx,*,role_name:str):
        fetch=discord.utils.get(ctx.guild.roles,name=role_name)
        if fetch is not None:
            try:
                await self.bot.aio.aio.execute("INSERT INTO sar VALUES(%s)",(fetch.name,))
                await ctx.send(f":check: Added {fetch.name} to self assignable roles")
            except Exception as e:
                em=discord.Embed(title="Error occured as below", description=e)
                await ctx.send(embed=em)
        else:
            await ctx.send(f":x: Role `{role_name}` not found. Make sure you enter role name in a **case sensitive** manner")

    @sar.command(name='deconfig', hidden=True)
    @commands.has_any_role('Lords', 'IU Bot Dev')
    async def _sar_delete(self,ctx,*,role_name:str):
        fetch=discord.utils.get(ctx.guild.roles,name=role_name)
        if fetch is not None:
            try:
                await self.bot.aio.aio.execute("DELETE FROM sar WHERE rolename=%s",(fetch.name,))
                await ctx.send(f":check: Deleted {fetch.name} from self assignable roles")
            except Exception as e:
                em=discord.Embed(title="Error occured as below", description=e)
                await ctx.send(embed=em)
        else:
            await ctx.send(f":x: Role `{role_name}` not found. Make sure you enter role name in a **case sensitive** manner")


        

def setup(bot):
    bot.add_cog(Roles(bot))
