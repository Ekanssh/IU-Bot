from discord.ext import commands
import discord


#look in starboard if message is already starred
#call edit_existing() if found 
#call create_new_entry() if not found
class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "\u2b50" or reaction.emoji == "🌟" :
            if reaction.message.channel.name == 'starboard' :
                total_reactions =  int(reaction.message.content.split()[1]) + reaction.count
                return await self.edit_existing(total_reactions,reaction.message)
            elif reaction.count > 2:
                return await self.starborad_lookup(reaction)

            
    async def starborad_lookup(self,reaction):
        message=reaction.message
        starboard=discord.utils.get(message.guild.channels, name='starboard')
        async for msg in starboard.history(limit=50):
            if msg.content.split()[4] == str(message.id):
                return await self.edit_existing(reaction.count,msg)
        return await self.create_new_entry(reaction)


    async def edit_existing(self,stars,msg):
        if stars > 2 and stars < 5:
            staremoji = ":star:"
        elif stars > 4 and stars < 8:
            staremoji = ":star2:"
        elif stars > 7 and stars < 12:
            staremoji = ":dizzy:"
        elif stars > 12:
           staremoji = ":sparkles:"

        channel_mention=msg.content.spilt()[2]
    
        await msg.edit(content=f"{staremoji} {stars} {channel_mention} Id: {reaction.message.id}")

    async def create_new_entry(self,reaction):
        message = reaction.message
        starboard=discord.utils.get(message.guild.channels, name='starboard')
        embed = discord.Embed(description=(message.content + f'\n[Jump!]({message.jump_url})'))
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url_as(format='png'))
        embed.timestamp = message.created_at
        embed.color = 0xFFDF00
        if message.embeds:
            data = message.embeds[0]
            if data.type == 'image':
                embed.set_image(url=data.url)
        if message.attachments:
            file = message.attachments[0]
            if file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                embed.set_image(url=file.url)
            else:
                embed.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)
        content = f":star: {reaction.count} {reaction.message.channel.mention} Id: {reaction.message.id}"
        await starboard.send(content,embed=embed)

def setup(bot):
    bot.add_cog(Starboard(bot))
