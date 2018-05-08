from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
from contextlib import redirect_stdout
import gspread
import io, os
import traceback, inspect
import asyncio, discord, aiohttp
import time, datetime
import math, random
import functools 
import textwrap,re
import sqlite3
import globalvars
import httplib2
import threading
import aiopg
import logging, signal
from PIL import Image, ImageFont, ImageDraw
from Paginator import Paginator
from time import localtime, strftime
from bs4 import BeautifulSoup as bs 
import aiohttp 
from time import localtime, strftime
import requests

# import bs4
# from bs4 import BeautifulSoup as bs

bot = commands.Bot(description='The offical bot overwatching Indians United.', command_prefix=['iu_', 'iu ', 'IU ', 'IU_', 'Iu ','Iu_'])

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
http = creds.authorize(httplib2.Http())
creds.refresh(http)
client = gspread.authorize(creds)
if creds.access_token_expired:
	client.login()

db = client.open("IU DB").sheet1
dsn = "dbname = 'd1b1qi3p5efneq' user='ynhburlpfyrfon' password='14e33018bf4991471bae5c11d2d57ab4424120299510a7891e61ee0123e81bc8' host='ec2-79-125-117-53.eu-west-1.compute.amazonaws.com'"
ownerid = [360022804357185537, 315728369369088003, 270898185961078785, 341958485724102668, 371673235395182592, 388984732156690433]

class aiopg_commands:
	async def connect(self):
		self.conn = await aiopg.connect(database='d1b1qi3p5efneq',
								   user='ynhburlpfyrfon',
								   password='14e33018bf4991471bae5c11d2d57ab4424120299510a7891e61ee0123e81bc8',
								   host='ec2-79-125-117-53.eu-west-1.compute.amazonaws.com')
		self.cursor = await self.conn.cursor()
		
	async def execute(self, statement, args:tuple = None):
		if args is None:
			await self.cursor.execute(statement)
		else:
			await self.cursor.execute(statement, args)
  
aio = aiopg_commands()
#custom functions for doing stuff goes here
def tdm(td):
	return ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)

def calculate_level(level: 'current level') -> 'xp to reach next level': 
	return (level**2+level)/2*100-(level*100) 


'''
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
	await ctx.message.channel.send(":x: | Sorry, you are on a cooldown. Try again in " + str(round(int(error.retry_after), 2)) + "s")
  else:
	logging.error(error, exc_info=True)
'''

@bot.event
async def on_ready():
	await bot.get_guild(globalvars.devServerID).get_channel(globalvars.logID).send("Bot load at:" + f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"+" :D")
	bot.load_extension("repl")
	bot.add_cog(General())
	bot.add_cog(Admin())
	bot.add_cog(Economy())
	bot.add_cog(Miscellaneous())
	await aio.connect()
	await aio.execute("CREATE TABLE IF NOT EXISTS Dailies(id BIGINT, dailiesCount INT, remaining_timestamp TIMESTAMP)")
	await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT)")
	
	await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="on Indians United [iu_help reveals commands]"))
	 
@bot.event
async def on_member_join(member):
	if member.guild.id == 281793428793196544:
		channel = bot.get_channel(429618676875001856)
		await channel.send('Welcome to IU United, '+member.mention+'! Please enjoy your time here and hope you check #rules! :)')

@bot.event
async def on_member_remove(member):
	if member.guild.id == 281793428793196544:
		channel = bot.get_channel(429618676875001856)
		await channel.send('We are feeling bad to see you leaving %s!' %(member.name))

@bot.event
async def on_message(msg):
	if msg.channel.name is globalvars.memesChannel:
		for chr in list(string.ascii_letters):
			if chr in str(msg.content):
				await msg.delete()
				
	found = False
	if not msg.author.bot:
		await aio.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
		for i in await aio.cursor.fetchall():
			if i is not None:
				if i[0] == msg.author.id:
				
					found = True
	
					await aio.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
					xp = (await aio.cursor.fetchall())[0][6]
					await aio.execute("UPDATE profile SET xp = %s WHERE id = %s", (xp + 5, msg.author.id, ))
		
					await aio.execute("SELECT * FROM profile WHERE id = %s", (msg.author.id, ))
					level = (await aio.cursor.fetchall())[0][4]
		
					if xp == int(calculate_level(level)):
						await aio.execute("UPDATE profile SET level = %s WHERE id = %s", (level + 1, msg.author.id, ))
						await msg.channel.send("Congratulations, " + msg.author.mention + " you advanced to level {}".format(level + 1),delete_after=10)
	if not found:
		if not msg.author.bot:
			await aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s)", (msg.author.id, 0, 'milky-way', 'None', 1, 'I am imperfectly perfect...', 0))

	await bot.process_commands(msg)

@bot.event
async def on_message_edit(before, after):
  await bot.process_commands(after)

	
class Admin:
	'''For administrative purposes'''
	
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
		
        @commands.command(hidden = True, name="sql")
        async def _sql(self, ctx, statement, *args):
            if not ctx.author.id in ownerid: return
            try: 
                if len(args) > 0: await aio.execute(statement, *args)
                else: await aio.execute(statement)
            except Exception as e: 
                await ctx.send(embed = discord.Embed(title="ERROR", description = "```" + e + "```")


class General:
	'''General commands'''  

	@commands.command(aliases=['iplscores', 'scores'])
	async def ipl(self , ctx) :
		url = "http://www.cricbuzz.com/"
		data = []
		async with aiohttp.ClientSession() as cs: 
			async with cs.get(url) as r:
				html = await r.read()
			soup = bs(html, 'html.parser')
		t = soup.find_all(attrs={'class':'cb-ovr-flo'})
		for u in t: 
			if u is not None :
				data.append(u.text)
		tossres = data[5]
		inn = [ data[2] , data[4] ]
		tm = [ data[1] , data[3] ]
		curr = data[0]
		em = discord.Embed(title = "{0} vs {1}".format(tm[0],tm[1]) , description = "{5} ... \nCurrent Inning : {0} \n{1} : {2}\n{3} : {4}".format(curr,tm[0],inn[0],tm[1],inn[1],tossres)+"\n*Score Updated at* "+str(strftime("%a, %d %H:%M:%S", localtime())), colour = int(hex(random.randint(0,16777215)),16))
		await ctx.send(embed = em)
		
	@commands.command(aliases = ['scoretable','ipltable','ipl_table','points','points_table','pt'])
	async def pointstable(self, ctx) :
		"""Displays the IPL Points Table """
		data = requests.get("http://www.cricbuzz.com//cricket-series/2676/indian-premier-league-2018/points-table")
		soup = bs.BeautifulSoup(data.text,"html.parser")
		data,tmd = [],[]
		teams = ['Delhi Daredevils','Royal Challengers Bangalore','Rajasthan Royals','Kolkata Knight Riders','Mumbai Indians','Chennai Super Kings','Sunrisers Hyderabad','Kings XI Punjab']
		i = 0
		for link in soup.find_all('td') :
			data.append(link.text)
		for i in range(len(data)) :
			if data[i] in teams :
				if len(data[i+1]) <= 2 :
					x = []
					for j in range(8) :
						x.append(data[i+j])
					tmd.append(x)
		table = ""
		for t in tmd :
			rank = str(tmd.index(t)+1)
			name,plyed,won,lost,points,NRR = t[0],t[1] , t[2] , t[3] , t[-2] , t[-1]
			table += str("\n"+rank + ") " + name + "\n\tP : " + plyed + "\t\tW : "+won+"\t\tL : "+lost+"\n\tP : "+points+"\t\tNRR = "+NRR)
		em = discord.Embed(title = "Points Table IPL 2018" , description = table , colour = int(hex(random.randint(0,16777215)),16) )
		await ctx.send(embed = em )
	
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def profile(self, ctx, mem: discord.Member = None):
		'''Check your or someone else's profile'''
		found = False
		mem = mem or ctx.message.author
		if mem.bot:
			await ctx.send("Sorry, bots don't have a profile... ~~*until they overthrow humans*~~")
			return 
		await aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id, ))
		for i in await aio.cursor.fetchall():
			if i is not None:
				if i[0] == mem.id:
				  found = True
				  await aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(mem.id), ))
				  if len(await aio.cursor.fetchall()) > 0:
					  await aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(mem.id), ))
					  currentDaily = int((await aio.cursor.fetchall())[0][1])
				  else :
					  currentDaily = 0
	  
				  await aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
				  level = (await aio.cursor.fetchall())[0][4]
	  
				  await aio.execute("SELECT * FROM profile WHERE id = %s", (mem.id,))
				  note = (await aio.cursor.fetchall())[0][5]
	  
				  back = Image.open("Images/background.png")
				  background = Image.open("Images/milky-way.jpg")
				  background = background.crop((0, 0, 500, 215))
				  back.paste(background, box = (0, 0))
				  font = ImageFont.truetype("Fronts/Quicksand-Regular.otf", 45)
				  badges_font = ImageFont.truetype("Fronts/Quicksand-Regular.otf", 25)
				  level_font = ImageFont.truetype("Fronts/Quicksand-Regular.otf", 25)
				  credits_reps_font = ImageFont.truetype("Fronts/Quicksand-Regular.otf", 20)
				  note_font = ImageFont.truetype("Fronts/Quicksand-Regular.otf", 20)
	  
				  d = ImageDraw.Draw(back)
				  d.rectangle([0, 160, 110, 270], fill = (255, 255, 255))
				  async with aiohttp.ClientSession() as cs:
					  async with cs.get(mem.avatar_url) as r:
						  with open("TEMPava.png", 'wb') as ava:
							  ava.write(await r.read())
				  avatar = Image.open("TEMPava.png")
				  avatar = avatar.resize((100, 100))
				  back.paste(avatar, (5, 165))    
				  d.text(text = str(mem), xy = (125, 215), font = font)
				  d.line([(113, 219), (113, 500)], fill = (50, 50, 50), width = 3) #line beside ava

				  d.line([(11, 302), (100, 302)], fill = (50, 50, 50), width = 3)
				  d.text(text = "Badges", xy = (10, 275), font = badges_font)
				  d.text(text = "Level:", xy = (360, 265), font = level_font)
				  d.text(text = str(level), xy = (435, 265), font = level_font)

				  d.text(text = "Credits:", xy = (135, 310), font = credits_reps_font)
				  d.text(text = str(currentDaily), xy = (435, 310), font = credits_reps_font, align = 'RIGHT')

				  d.text(text = "Reputations:", xy = (135, 340), font = credits_reps_font)
				  d.text(text = "-", xy = (435, 340), font = credits_reps_font, align = 'RIGHT')

				  d.rectangle([135, 400, 480, 490])
				  d.text(text = note, xy = (145, 405), font = note_font)
				  back.save(str(mem.name) + '.png')
				  await ctx.send(file = discord.File(str(mem.name) + '.png'))
				  os.remove(str(mem.name) + '.png')
				  os.remove('TEMPava.png')

		if not found:
			await aio.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s, %s, %s)", (mem.id, 0, 'milky-way', 'None', 1, 'I am imperfectly perfect...', 0))
			await ctx.invoke(bot.get_command("profile"), mem)
	   
		
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def note(self, ctx, option="show", *, newNote = None):
		 '''Set your profile's note'''
		 if ctx.message.author.bot:
		   return 
		 if option == "show":
			 await aio.execute("SELECT * FROM profile WHERE id = %s", (ctx.message.author.id,))                      
			 note =  (await aio.cursor.fetchall())[0][5]
			 await ctx.send("Your current note is:\n" + "```" + note + "```")
		 elif option == "set" and newNote is not None:
			 await aio.execute("UPDATE profile SET note = %s WHERE id = %s", (newNote, ctx.message.author.id, ))
			 await ctx.send("Your current note is:\n" + "```" + newNote + "```")
		 elif option == "reset":
			 await aio.execute("UPDATE profile SET note = %s WHERE id = %s", ('I am imperfectly perfect...', ctx.message.author.id, ))  
			 await ctx.send("Your profile's note has been reset to:\n" + '```I am imperfectly perfect...```')
	'''        
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def top(self, ctx):
		#Check who tops the local server's Scoreboard
		msg = await ctx.send("*Please wait until I gather people's information*")
		page_index = 1
		embed_list = []
		await aio.execute("SELECT id, xp FROM profile")
		rows_count = len(await aio.cursor.fetchall())
		row_index = 1
		async with aiopg.create_pool(dsn) as pool:
			async with pool.acquire() as conn:
				async with conn.cursor() as c:
					await c.execute("SELECT id, xp FROM profile ORDER BY xp DESC LIMIT %s OFFSET %s", (10, 10-10))
					for l in await c.fetchall():
						name = (await bot.get_user_info(l[0])).name
						await ctx.send(name)


		for i in range (10, rows_count, 10):
			await aio.execute("SELECT id, xp FROM profile ORDER BY xp DESC LIMIT %s OFFSET %s", (i, i-10))
			em = discord.Embed(title = "Scoreboard for " + ctx.guild.name, 
									color = 0x00FFFF,
									description = '')
			position = 0
			for l in await aio.cursor.fetchall():
				try:
					name = (await bot.get_user_info(l[0])).name
					em.description += name + ' ' * (29 - len(name)) + ':: ' + str(l[6]) + '\n'
					if l[0] == ctx.message.author.id:
						position = row_index
					row_index += 1
				except:
					em.description += "Couldn't find user. Discord id: `{}`".format(l[0])
			em.add_field(name = ctx.message.author.name, value = "\n\nYour position in " + ctx.guild.name + " is " + str(position))
			em.set_footer(text="Page {0} of {1}".format(page_index, int(rows_count/10)))
			page_index += 1
			embed_list.append(em)
			
			
		info_embed = discord.Embed(title = "Help Info", 
								   description = "\u23EA:  Go to the first page\n\u25C0:  Go to the previous page\n\u23F9:  Stop the help command\n\u25B6:  Go to the next page\n\u23E9:  Go to the last page\n\U0001f522:  Asks for a page number\n\u2139:  Shows this info", 
								   colour = 0x2279DE)  
		embed_list.append(info_embed)
		await msg.edit(embed = embed_list[0])
		pa = Paginator(bot, msg, ctx.message.author, 0)
		await pa.paginate(embed_list)
	'''    
		
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def ping(self, ctx):
		'''Call the bot'''
		msg = await ctx.send(ctx.author.mention+', Pong!')
		res = msg.created_at - ctx.message.created_at
		res = tdm(res)
		await msg.edit(content=ctx.author.mention+', Pong! :ping_pong: Took {} ms'.format(res))
	
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def say(self, ctx, *, something: commands.clean_content='IU Bot Bot here!'):
		'''The bot becomes your copycat'''
		await ctx.send(something)
		await ctx.message.delete()
   
	@commands.command()
	#dont dare to touch this command
	async def bday(self, ctx, bDay):
		try:
			db.find(str(ctx.message.author.id))
			await ctx.message.add_reaction('\u274C')
		except:
			userID = str(ctx.message.author.id)
			db.insert_row([userID, bDay], index=1, value_input_option='RAW')
			await ctx.message.add_reaction('\u2705')
	
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def now(self, ctx):
		'''Get current date and time'''
		m = str(datetime.datetime.now()).split()
		embed = discord.Embed(title='Date-time information',
							  color=eval(hex(ctx.author.color.value)))
		embed.add_field(name='Date', value='{}'.format(m[0]))
		embed.add_field(name='Time', value='{}GMT'.format(m[1]))
		await ctx.send(embed=embed)
	
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command(name = '8ball')
	async def _func(self, ctx, *, question = ' '):
		'''the bot entertains you with nonsense'''
		if question[-1] == '?':
			return await ctx.send(random.choice(globalvars.ballAnswers))
		await ctx.send('`Try again with a question!`')
	
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def choose(self, ctx, *, options):
		'''randomly gets a choice from a list of choices separated with '|' '''
		if len(options.split('|')) >= 2:
			return await ctx.send(embed=discord.Embed(title="And the bot has chosen...",description=random.choice(options.split('|')),color=discord.Color.gold()))
		await ctx.send(embed=discord.Embed(title='You invoked command incorrectly!',description='Give at least two options separated by **|**',color=discord.Color.red()))
	 
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
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

class Economy:
	@commands.command()
	async def level(self,ctx,person:discord.Member=None):
		'''get your XP and level stats'''
		if person is None:person=ctx.author
		searchable=str(person.id)
		await aio.execute("SELECT * FROM profile WHERE id = {}".format(searchable))
		temp = (await aio.cursor.fetchall())[0]
		level, xp = temp[4],temp[6]
		if xp<1000:embed=discord.Embed(title=person.name+"'s level",description="Level "+str(level)+"\n"+str(xp)+" xp",colour=discord.Colour.from_rgb(205, 127, 50))
		elif xp<5000:embed=discord.Embed(title=person.name+"'s level",description="Level "+str(level)+"\n"+str(xp)+" xp",colour=discord.Colour.from_rgb(218, 218, 218))
		elif xp<10000:embed=discord.Embed(title=person.name+"'s level",description="Level "+str(level)+"\n"+str(xp)+" xp",colour=discord.Colour.gold())
		else:embed=discord.Embed(title=person.name+"'s level",description="Level "+str(level)+"\n"+str(xp)+" xp",colour=discord.Colour.from_rgb(20, 30, 179))
		await ctx.send(embed=embed)
		
		
	@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
	@commands.command(aliases=['daily'])
	async def dailies(self, ctx):
            '''Get your free ₹200'''
            if ctx.message.author.bot:
                  await ctx.send("Sorry, bots have nothing to do with money")
                  return 
            msg_timestamp = ctx.message.created_at
            found = False
            await aio.execute("SELECT * FROM Dailies WHERE id= %s", (ctx.message.author.id, ))

            for i in await aio.cursor.fetchall():
                  if i is not None:
                        if i[0] == ctx.message.author.id:
                              found = True
                              await aio.execute("SELECT * FROM Dailies WHERE id= %s", (ctx.message.author.id, ))
                              previous_msg_timestamp = (await aio.cursor.fetchall())[0][2]
                              
                              remaining_timestamp = previous_msg_timestamp - msg_timestamp
			
                              await aio.execute("SELECT * FROM Dailies WHERE id= %s", (ctx.message.author.id, ))
                              currentDaily = int((await aio.cursor.fetchall())[0][1])
                             
                              secondsRemaining = remaining_timestamp.seconds
                              time = str(datetime.timedelta(seconds = secondsRemaining)).split(":")
                              
                              if secondsRemaining >= 86400:                              
                                    currentDaily += 200
                                    await aio.execute("UPDATE Dailies SET dailiesCount = %s, remaining_timestamp = %s WHERE id = %s", (currentDaily, msg_timestamp, ctx.message.author.id, ))
                                    await ctx.send(":moneybag: | You got your 200 dialies!\n You have ₹{}".format(currentDaily))
                        
                              else:
                                    await ctx.send("Sorry, you can claim your dailies in {0}hrs, {1}mins, {2}s\nYou have ₹{3}:moneybag:".format(time[0], time[1], time[2], currentDaily))

            if not found:
                  await aio.execute("INSERT INTO Dailies VALUES (%s, '200', %s)", (ctx.message.author.id, msg_timestamp))
                  await ctx.send(":moneybag: | You got your 200 dialies!\nYou have ₹200")
			
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@commands.command()
	async def credits(self, ctx, otherMem: discord.Member = None):
		'''Check your or someone else's credits'''
		if ctx.message.author.bot or (otherMem is not None and otherMem.bot):
			await ctx.send("Sorry, bot have nothing to do with money")
			return 
		found_in_db = False
		if otherMem is None:
			await aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(ctx.message.author.id),))
			for i in await aio.cursor.fetchall():
				if i is not None:
					if i[0] == str(ctx.message.author.id):
						found_in_db = True
						await aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(ctx.message.author.id),))                       
						await ctx.send(":moneybag: | You currently have ₹{0}".format((await aio.cursor.fetchall())[0][1]))
			if not found_in_db:
				await ctx.send(":moneybag: | You currently have ₹0")
		else:
			await aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(otherMem.id),))
			for i in await aio.cursor.fetchall():
				if i is not None:
					if i[0] == str(otherMem.id):
						found_in_db = True
						await aio.execute("SELECT * FROM Dailies WHERE id = %s", (str(otherMem.id),))                       
						await ctx.send(":moneybag: | {0} currently has ₹{1}".format(otherMem.name, (await aio.cursor.fetchall())[0][1]))
			if not found_in_db:
				await ctx.send(":moneybag: | {0} currently has ₹0".format(otherMem.name))
'''	
async def dailiesCounter():
	await bot.wait_until_ready()
	await aio.connect()
	await aio.execute("CREATE TABLE IF NOT EXISTS Dailies(id BIGINT, dailiesCount INT, remaining_timestamp TIMESTAMP)")
	await aio.execute("CREATE TABLE IF NOT EXISTS profile(id BIGINT, reps INT, profile_background TEXT, badges TEXT, level INT, note TEXT, xp INT)")
	while not bot.is_closed():
		await aio.execute("SELECT * from Dailies")
		for i in await aio.cursor.fetchall():
			if not int(i[2]) <= 0:
				tempTime = int(i[2]) - 2
				await aio.execute("UPDATE Dailies SET secToReset = %s WHERE id = %s", (str(tempTime), str(i[0]), ))
		await asyncio.sleep(2)
'''
			
			
class Miscellaneous:
	@commands.command(aliases=['fb'])
	async def feedback(self,ctx,*,message):
		'''Please provide any feedback and report any bugs.'''
		author=ctx.message.author.name+" said in "+"'"+ctx.guild.name+"'"
		await bot.get_guild(381052278708240385).get_channel(435375286385770497).send(embed=discord.Embed(color=eval(hex(ctx.author.color.value)),title=author,description="#"+ctx.channel.name+":\n"+message))
		await ctx.message.add_reaction('\u2705')
		

bot.run(globalvars.TOKEN)
