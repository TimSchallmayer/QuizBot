import discord as dc
from discord.ext import commands

class check_questions(commands.Cog):
    def __init__(self, bot, answer, channel):
        self.bot = bot
        self.answer = answer
        self.channel = channel

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
        if msg.content.lower() == answer1.lower():
            self.bot.send_message_allowed = False
            await msg.add_reaction("✅")
            embed_correct_answer = dc.Embed(title="✅ Frage beantwortet ✅", description=f"Glückwunsch {user.mention}, deine Antwort ist richtig!\n\nDie richtige Antwort lautet: **{answer1}**", color=0x00D166)
            await msg.channel.send(embed=embed_correct_answer)
        else:
            self.bot.send_message_allowed = True
            await msg.add_reaction("❌")


async def setup(bot):
    pass