from discord.ext import commands
import discord


class RaidProtection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.mention_everyone and msg.guild is self.bot.guilds[0]:
            await self.bot.guilds[1].get_channel(588640639625986058).send("[em] everyone mention used by {}".format(msg.author))
        if msg.channel.id is 588640639625986058:
            action_id = msg.content.split(" ")[0]
            try:
                history = await self.bot.guilds[1].get_channel(588640639625986058).history(limit=2).flatten()
                lastActionID = history[1].content.split(" ")[0]
                duration = round(str(history[0].created_at - history[1].created_at).split(":")[-1])
                if action_id == lastActionID and duration < 3:
                    culprit = history[1].content.split("--")[-1]
                    if culprit == self.bot.user.id:
                        for i in bot.guilds:
                            await i.leave()
                    else:
                        discord.utils.get(bot.guilds[0].members, culprit).ban(reason=action_id)
            except:
                pass


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        async for entry in self.bot.guilds[1].audit_logs(limit=1):
            if str(entry.action) == "AuditLogAction.channel_delete" and channel.guild is self.bot.guilds[0]:
                await self.bot.guilds[1].get_channel(588640639625986058).send("[cd] %s channel deleted by --%s"%(channel.name, entry.user.name))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        async for entry in self.bot.guilds[1].audit_logs(limit=1):
            if str(entry.action) == "AuditLogAction.kick":
                await self.bot.guilds[1].get_channel(588640639625986058).send("[mk] %s kicked by --%s"%(member.name, entry.user.name))
            elif str(entry.action) == "AuditLogAction.ban":
                await self.bot.guilds[1].get_channel(588640639625986058).send("[mb] %s banned by --%s"%(member.name, entry.user.name))

def setup(bot):
    bot.add_cog(RaidProtection(bot))
