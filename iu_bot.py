from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
from contextlib import redirect_stdout
import gspread
import io
import traceback, inspect
import asyncio, discord, aiohttp
import time, datetime
import math, random
import functools 
import textwrap,re
import sqlite3
import globalvars
import httplib2
# import bs4
# from bs4 import BeautifulSoup as bs

bot = commands.Bot(description='The offical bot overwatching Indians United.', command_prefix='iu_')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
http = creds.authorize(httplib2.Http())
creds.refresh(http)
client = gspread.authorize(creds)
db = client.open("IU DB").sheet1

conn = sqlite3.connect("dailies.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Dailies(id TEXT, dailiesCount TEXT, secToReset TEXT)")

def tdm(td):
    return ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)

class Admin:
    '''For administrative purposes'''
    @commands.command()
    @commands.has_permissions(kick_members=True) 
    async def kick(self, ctx, member: discord.Member):
        '''Kick members from your server'''
        try:
            await member.kick()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        '''Ban toxic members from your server'''
        try:
            await member.ban()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

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
    async def purge(self, ctx, number):
        '''Clears specified number of messages, ranging from 2 to 100'''
        await ctx.channel.purge(limit=number)


class General:
    '''General commands'''
    
    @commands.command(aliases=['daily'])
    async def dailies(self, ctx):
        found = False
        for i in c.execute("SELECT * FROM Dailies WHERE id=?", (str(ctx.message.author.id),)):
            if i[0] == str(ctx.message.author.id):
                found = True
                c.execute("SELECT * FROM Dailies WHERE id=?", (str(ctx.message.author.id),))
                currentDaily = int(c.fetchall()[0][1])
                c.execute("SELECT * FROM Dailies WHERE id=?", (str(ctx.message.author.id),))
                secondsRemaining = int(c.fetchall()[0][2])
                time = str(datetime.timedelta(seconds = secondsRemaining)).split(":")
            
                if secondsRemaining <= 0:                              
                    currentDaily += 200
                    c.execute("UPDATE Dailies SET dailiesCount = " + str(currentDaily) + ", secToReset = '86400' WHERE id =" + str(ctx.message.author.id))
                    conn.commit()
                    await ctx.send("You got your 200 dialies! :moneybag:\n You have ₹{}".format(currentDaily))
                
                else:
                    ctx.send("Sorry, you can claim your dailies in {0}hrs, {1}mins, {2}s\n You have ₹{}".format(time[0], time[1], time[2], currentDaily))
        if not found:
            c.execute("INSERT INTO Dailies VALUES (" + str(ctx.message.author.id) + ',' + "200" + ',' + "86400" + ")")
            conn.commit()
            await ctx.send("You got your 200 dialies! :moneybag:\n You have ₹200")
                
    
    @commands.command()
    async def ping(self, ctx):
        '''Call the bot'''
        msg = await ctx.send(ctx.author.mention+', Pong!')
        res = msg.created_at - ctx.message.created_at
        res = tdm(res)
        await msg.edit(content=ctx.author.mention+', Pong! :ping_pong: Took {} ms'.format(res))

    @commands.command()
    async def say(self, ctx, *, something: commands.clean_content='IU Bot Bot here!'):
        '''The bot becomes your copycat'''
        await ctx.send(something)
        await ctx.message.delete()

    @commands.command()
    async def bday(self, ctx, bDay):
        try:
            db.find(str(ctx.message.author.id))
            await ctx.message.add_reaction('\u274C')
        except:
            userID = str(ctx.message.author.id)
            dbt.insert_row([userID, bDay], index=1, value_input_option='RAW')
            await ctx.message.add_reaction('\u2705')

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
        '''the bot entertains you with nonsense'''
        if question[-1] == '?':
            return await ctx.send(random.choice(globalvars.ballAnswers))
        await ctx.send('`Try again with a question!`')
    
    @commands.command()
    async def choose(self, ctx, *, options):
        '''randomly gets a choice from a list of choices separated with '|' '''
        if len(options.split('|')) >= 2:
            return await ctx.send(embed=discord.Embed(title="And the bot has chosen...",description=random.choice(options.split('|')),color=discord.Color.gold()))
        await ctx.send(embed=discord.Embed(title='You invoked command incorrectly!',description='Give at least two options separated by **|**',color=discord.Color.red()))
            
    @commands.command()
    async def rps(self, ctx, value):
        '''Play Rock Paper Scissors with the bot'''
        options = ['Rock', 'Paper', 'Scissors', 'Rock'];
        value = value.title()
        if value not in options:
            return await ctx.send('You can choose from %s only'%(', '.join(options[:3])))
        guess = random.choice(options[:3])
        i = options.index(value)
        if value is guess:
            res = 'It\'s a tie!'
        elif value == "Rock" and guess == "Rock":
            res = "It's a tie!"
        else:
            if guess is options[i+1]:
                res = 'You lost'
            else:
                res = 'You won'
        return await ctx.send('**Bot**: %s\n**You**: %s\n%s'%(guess, value, res))

'''REPL'''
ownerid = [360022804357185537, 315728369369088003, 270898185961078785, 341958485724102668, 371673235395182592, 388984732156690433] #pls add names in the same order. Last: Yash

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
        if ctx.message.author.id not in ownerid:
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
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="on Indians United [iu_help reveals commands]"))
    
async def dailiesCounter():
    await bot.wait_until_ready()
    while not bot.is_closed:
        for i in c.execute("SELECT * from Dailies"):
            if not i[2] <= 0:
                tempTime = int(i[2]) - 1
                c.execute("UPDATE Dailies SET secToReset = " + str(tempTime) + "WHERE id = " + str(i[0]))
                conn.commit()
                await asyncio.sleep(2)           #update every 2 secs. Let ma boi have some time
    
bot.loop.create_task(dailiesCounter())
bot.run(globalvars.TOKEN)
