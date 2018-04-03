import asyncio, discord, math, random, time, datetime, aiohttp, functools, inspect, re
from discord.ext import commands
import traceback
import inspect
import textwrap
from contextlib import redirect_stdout
import io
# import bs4
# from bs4 import BeautifulSoup as bs

import globalvars

bot = commands.Bot(description='The offical bot overwatching Indians United.', command_prefix='iu_')

def tdm(td):
    return ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)

class Admin:
    '''For administrative purposes'''
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
    async def purge(self, ctx, number):
        '''Clears specified number of messages, ranging from 2 to 100'''
        await ctx.channel.purge(limit=number)


class General:
    '''General commands'''
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
    async def _func(self, ctx, *, question = ' '):
        if question[-1] == '?':
            return await ctx.send(random.choice(globals.ballAnswers))
        await ctx.send('`Try again with a question!`')
    
    @commands.command()
    async def choose(self, ctx, *, options):
        if len(options.split('|')) >= 2:
            return await ctx.send(random.choice(options.split('|')))
        await ctx.send('Give atleast two options separated by **|**')
            


'''REPL'''
ownerid = [360022804357185537,315728369369088003,270898185961078785]

class REPL():

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        'Automatically removes code blocks from the code.'
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:(- 1)])
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(hidden=True, name='exec')
    async def _eval(self, ctx, *, body: str):
        '''for bot owner to execute statements'''
        if ctx.author.id not in ownerid:
            return
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'server': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')
        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            await ctx.message.add_reaction('\u274C')
            value = stdout.getvalue()
            await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass
            if ret is None:
                if value:
                    await ctx.send('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                await ctx.send('```py\n%s%s\n```' % (value, ret))

    @commands.command(hidden=True)
    async def repl(self, ctx):
        '''for bot owner to run series of commands'''
        if ctx.author.id not in ownerid:
            return
        msg = ctx.message
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'server': msg.guild,
            'channel': msg.channel,
            'author': msg.author,
            '_': None,
        }
        if msg.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel. Exit it with `quit`.')
            return
        self.sessions.add(msg.channel.id)
        await ctx.send('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for('message', check=(lambda m: m.content.startswith('`') and m.author.id == ownerid and m.channel == ctx.channel))
            cleaned = self.cleanup_code(response.content)
            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(msg.channel.id)
                return
            executor = exec
            if cleaned.count('\n') == 0:
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval
            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue
            variables['message'] = response
            fmt = None
            stdout = io.StringIO()
            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = '```py\n{}{}\n```'.format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = '```py\n{}{}\n```'.format(value, result)
                    variables['_'] = result
                elif value:
                    fmt = '```py\n{}\n```'.format(value)
            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await msg.channel.send('Content too big to be printed.')
                    else:
                        await msg.channel.send(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await msg.channel.send('Unexpected error: `{}`'.format(e))

'''Added'''


@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name is globalvars.welcomeName:
            await bot.send_message(channel, 'Welcome to IU United, '+member.mention+'! Please enjoy your time here and hope you check #rules! :)')

@bot.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name is globalvars.leaveName:
            await ctx.send_message(channel, 'We are feeling bad to see you leaving %s!' %(member.name))

@bot.event
async def on_message(ctx):
    if ctx.channel.name is globalvars.memesChannel:
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
    bot.add_cog(REPL(bot))

bot.run(globalvars.TOKEN)
