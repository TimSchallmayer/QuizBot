import discord as dc
from discord.ext import commands

class check_questions(commands.Cog):
    def __init__(self, bot, answer, channel, user: dc.Member, author: dc.Member):
        self.bot = bot
        self.answer = answer
        self.channel = channel
        self.user = user
        self.author = author

    @commands.Cog.listener()
    async def on_message(self, msg):
        if self.bot.send_message_allowed == False:
            return
        if msg.author == self.bot.user:
            return
        if msg.channel != self.channel:
            return
        
        if self.bot.send_message_allowed and msg.author != self.bot.user:
            await self.check_answer(msg, msg.author, self.answer)

    async def check_answer(self, msg, user: dc.Member, answer1: str):
        if answer1.lower() in msg.content.lower():
            self.bot.send_message_allowed = False
            await msg.add_reaction("✅")
            embed_correct_answer = dc.Embed(title="✅ Frage beantwortet ✅", description=f"Glückwunsch {user.mention}, deine Antwort ist richtig!\n\nDie richtige Antwort lautet: **{answer1}**\n\n **Aktueller Punktestand**\n {self.author.mention}:  \n {self.user.mention}:  \n", color=0x00D166)
            await msg.channel.send(embed=embed_correct_answer)
        else:
            self.bot.send_message_allowed = True
            await msg.add_reaction("❌")


async def setup(bot):
    pass