import discord as dc
from discord.ext import commands
from rapidfuzz import fuzz
import random

class check_questions(commands.Cog):
    def __init__(self, bot, answer, channel, user: dc.Member, author: dc.Member, difficulty):
        self.bot = bot
        self.answer = answer
        self.channel = channel
        self.user = user
        self.author = author
        self.difficulty = difficulty

    @commands.Cog.listener()
    async def on_message(self, msg):
        if self.bot.send_message_allowed == False and msg.author != self.bot.user:
            await msg.delete()
            return
        if msg.channel != self.channel:
            return
        if msg.author.bot:
            return
        
        await self.check_answer(msg, msg.author, self.answer)

    async def check_answer(self, msg, user: dc.Member, answer1: str):
        answer3 = answer1.lower().strip()
        answer = answer3.replace(" ", "")
        msg_content = msg.content.lower().strip()
        if fuzz.ratio(answer, msg_content) >= 80 and len(answer.strip()) >= 5 or fuzz.ratio(answer, msg_content) >= 75 and len(answer.strip()) >= 10 or fuzz.ratio(answer, msg_content) >= 70 and len(answer.strip()) >= 15 or fuzz.ratio(answer, msg_content) >= 65 and len(answer.strip()) >= 20 or fuzz.ratio(answer, msg_content) >= 60 and len(answer.strip()) >= 25 or answer == msg_content:
            await msg.add_reaction("✅")
            punkte = self.bot.points_author if user == self.author else self.bot.points_user
            if self.difficulty == "EASY":
                punkte += random.randint(3, 5)
            if self.difficulty == "MEDIUM":
                punkte += random.randint(8, 10)
            if self.difficulty == "HARD":
                punkte += random.randint(13, 15)
            
            if user == self.author:
                self.bot.points_author = punkte
            else:
                self.bot.points_user = punkte
            
            embed_correct_answer = dc.Embed(title="✅ Frage beantwortet ✅", description=f"Glückwunsch {user.mention}, deine Antwort ist richtig!\n\nDie richtige Antwort lautet: **{answer1}**\n\n **Aktueller Punktestand**\n {self.author.mention}: {self.bot.points_author} \n {self.user.mention}: {self.bot.points_user}\n", color=0x00D166)
            await msg.channel.send(embed=embed_correct_answer)
            self.bot.send_message_allowed = False
        else:
            self.bot.send_message_allowed = True
            await msg.add_reaction("❌")


async def setup(bot):
    pass