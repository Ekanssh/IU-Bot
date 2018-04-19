import discord, asyncio


class Paginator:
    '''A simple Paginator class for discord.Message object'''

    def __init__(self, bot, message: discord.Message, user:discord.Member, index):
        self.bot = bot
        self.message = message
        self.user = user
        self.index = index


    async def paginate(self, list_to_paginate: list):
        emoji_list = "\u23EA \u25C0 \u23F9 \u25B6 \u23E9 \U0001f522 \u2139".split()
        await self.bot.edit_message(self.message, '** **')
        for i in emoji_list:
            await self.bot.add_reaction(self.message, i)
            await asyncio.sleep(0.3)
        while True:
            r = await self.bot.wait_for_reaction(emoji_list, user = self.user)
            
            if r.reaction.emoji == emoji_list[0]:
                self.index = 0

            elif r.reaction.emoji == emoji_list[1]:
                if not self.index <= 0:
                    self.index -= 1
                else:
                    self.index = 0

            elif r.reaction.emoji == emoji_list[2]:
                await self.bot.delete_message(self.message)
                break

            elif r.reaction.emoji == emoji_list[3]:
                if not self.index >= len(list_to_paginate) - 2:
                    self.index += 1
                else:
                    self.index = len(list_to_paginate) - 2

            elif r.reaction.emoji == emoji_list[4]:
                self.index = len(list_to_paginate) - 2

            elif r.reaction.emoji == emoji_list[5]:
                bot_msg = await self.bot.say("Choose a number between 0 to {} to move to that page.".format(len(list_to_paginate)))
                msg = await self.bot.wait_for_message(timeout = 10, author = self.user)
                await self.bot.delete_message(bot_msg)

                if msg is not None:
                    try:
                        msg_index = int(msg.content)- 1
                        if not msg_index > 0 and msg_index < len(list_to_paginate):
                            bot_msg = await self.bot.say("Wrong input. Choose a number between 0 to {} to move to that page.".format(len(list_to_paginate)))
                            await asyncio.sleep(4)
                            await self.bot.delete_message(bot_msg)
                            
                        else:
                            self.index = msg_index 

                    except ValueError:
                        bot_msg = await self.bot.say("Wrong input. Choose a number between 0 to {} to move to that page.".format(len(list_to_paginate)))
                        await asyncio.sleep(4)
                        await self.bot.delete_message(bot_msg)
                    
                    try:
                        await self.bot.delete_message(msg)
                    except:
                        pass

                else: 
                    await self.bot.say("You did not chose a number :<\nI got bored")


            elif r.reaction.emoji == emoji_list[6]:
                self.index = len(list_to_paginate) - 1

            try:
                await self.bot.remove_reaction(self.message, r.reaction.emoji, self.user)
            except:
                pass
            
            #edit message everytime
            await self.bot.edit_message(self.message, embed = list_to_paginate[self.index], new_content = '')

