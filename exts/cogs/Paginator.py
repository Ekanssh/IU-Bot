import discord, asyncio


class Paginator:
    '''A simple Paginator class for discord.Message object'''

    def __init__(self, bot, message: discord.Message, user:discord.Member, index):
        self.bot = bot
        self.message = message
        self.user = user
        self.index = index


    async def paginate(self, list_to_paginate: list):
        c = await self.bot.get_context(self.message)
        emoji_list = "\u23EA \u25C0 \u23F9 \u25B6 \u23E9 \U0001f522 \u2139".split()

        #just a hack to see if the pagination is being done for the banner command, in which case, we need an additional 
        #'tick' emoji to buy a banner
        if self.message.content == "**Making the deck ready...**":
            emoji_list.append("\u2714")

        await self.message.edit(content = '** **')
        for i in emoji_list:
            await self.message.add_reaction(i)
            await asyncio.sleep(0.3)
        def check(reaction, user):
            return user == self.user and reaction.emoji in emoji_list and reaction.message.id == self.message.id
        while True:
            r, u = await self.bot.wait_for('reaction_add', check = check)

            if r.emoji == emoji_list[0]:
                self.index = 0

            elif r.emoji == emoji_list[1]:
                if not self.index <= 0:
                    self.index -= 1
                else:
                    self.index = 0

            elif r.emoji == emoji_list[2]:
                await self.message.delete()
                if len(emoji_list) == 8: #if pagination is for banner command
                    self.item_purchased = False
                break

            elif r.emoji == emoji_list[3]:
                if not self.index >= len(list_to_paginate) - 2:
                    self.index += 1
                else:
                    self.index = len(list_to_paginate) - 2

            elif r.emoji == emoji_list[4]:
                self.index = len(list_to_paginate) - 2

            elif r.emoji == emoji_list[5]:
                bot_msg = await c.send("Choose a number between 0 to {} to move to that page.".format(len(list_to_paginate)))
                def check_msg(message):
                    return message.author == self.user
                msg = await self.bot.wait_for('message', timeout = 10, check = check_msg)
                await msg.delete()

                try:
                    try:
                        msg_index = int(msg.content)- 1
                        if not msg_index >= 0 and msg_index < len(list_to_paginate):
                            bot_msg = await c.send("Wrong input. Choose a number between 0 to {} to move to that page.".format(len(list_to_paginate)))
                            await asyncio.sleep(4)
                            await bot_msg.delete()

                        else:
                            self.index = msg_index

                    except ValueError:
                        bot_msg = await c.send("Wrong input. Choose a number between 0 to {} to move to that page.".format(len(list_to_paginate)))
                        await asyncio.sleep(4)
                        await bot_msg.delete()

                    try:
                        await msg.delete()
                    except:
                        pass

                except asyncio.TimeoutError:
                    await c.send("You did not chose a number :<\nI got bored")


            elif r.emoji == emoji_list[6]:
                self.index = len(list_to_paginate) - 1

            if len(emoji_list) == 8:
                if r.emoji == emoji_list[7]:
                    self.item_purchased = True
                    try:
                        await self.message.delete()
                    except: pass
                    break

            try:
                await self.message.remove_reaction(r.emoji, self.user)
            except:
                pass

            #edit message everytime
            if isinstance(list_to_paginate[self.index], discord.Embed):
                await self.message.edit(new_content = '', embed = list_to_paginate[self.index])
            else:
                await self.message.edit(new_content = list_to_paginate[self.index])

