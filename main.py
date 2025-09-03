import discord as dc # type: ignore
from discord.ext import commands # type: ignore
from discord.ui import Button # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import asyncio
from cogs.duel_requests import duel_requests as duel_requests_class
from cogs.database_punkte import Punkte as punkte_class
#import logging
#logging.basicConfig(level=logging.DEBUG)

invitelink = None
inviteguild = None

load_dotenv()
Token = os.getenv("DISCORD_BOT_TOKEN")

intents = dc.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents
)

_disabled = False
string = ""
string_list = []
string1 = ""
string1_list = []
anzahlfragen = 0
list_of_kategories = []
list_of_difficulties = []
string_of_kategories = ""
string_of_difficulties = ""
answer = ""
antwort = {}
send_message_allowed = False

"""
class Quiz_Modal(dc.ui.Modal):
    global answer

    def __init__(self, user: dc.Member, question: str, answer1: str):
        super().__init__()
        self.user = user
        self.question = question
        self.answer = dc.ui.TextInput(label="Antwort", placeholder="Gib deine Antwort hier ein", required=True)
        self.answer1 = answer1
        self.add_item(self.answer)
        self.is_timeout = False
        self.is_timeout_counter = 0

    async def on_submit(self, interaction: dc.Interaction):
        global antwort

        while self.user not in antwort and self.is_timeout_counter < 180:
            await asyncio.sleep(1)
            self.is_timeout_counter += 1
            
        if self.is_timeout_counter >= 180:
                self.is_timeout = True       
        
        emdbed_antwort = dc.Embed(title="Antwort eingereicht", description=f"{self.user.mention} hat die Antwort auf die Frage '{self.question}' eingereicht: {self.answer.value}", color=0x00D166)
        await interaction.response.send_message(embed=emdbed_antwort, ephemeral=True)
        if self.answer.value.lower() == self.answer1.lower() and not self.is_timeout:
            embed_richtig = dc.Embed(title="Richtige Antwort", description=f"{self.user.mention} hat die richtige Antwort auf die Frage '{self.question}' eingereicht: {self.answer.value}", color=0x00D166)
            antwort[self.user] = embed_richtig
            
        elif self.answer.value.lower() != self.answer1.lower() and not self.is_timeout:
            embed_falsch = dc.Embed(title="Falsche Antwort", description=f"{self.user.mention} hat die falsche Antwort auf die Frage '{self.question}' eingereicht: {self.answer.value}", color=0xF93A2F)
            antwort[self.user] = embed_falsch

        elif self.is_timeout:
            embed_timeout = dc.Embed(title="Antwortzeit abgelaufen", description=f"{self.user.mention} hat nicht rechtzeitig auf die Frage '{self.question}' geantwortet.", color=0x597E8D)
            antwort[self.user] = embed_timeout
"""


@bot.slash_command()
async def duel(msg, user: dc.Member):
    
    class_of_duel_requests = duel_requests_class(bot)
    await class_of_duel_requests.duel_request(msg, user)

@bot.slash_command(guild_ids=[1157386757684338808])
async def leaderboard(msg, rang : int):
    string_leader = ""
    punkt = punkte_class(bot)
    leaderboard = await punkt.get_leaderboard(rang)
    for users in leaderboard:
        user = bot.get_user(users[0])
        if user is None:
            user = await bot.fetch_user(users[0])
        string_leader += f"{user.mention} - {users[1]} Punkte\n"
    embed = dc.Embed(title=f"🏆 Top {rang} Spieler 🏆", description=string_leader, color=0xFFD500)
    await msg.respond(embed=embed, ephemeral=True)

@bot.slash_command(guild_ids=[1157386757684338808])
@commands.has_permissions(administrator=True)
async def remove(ctx, user : dc.Member):
    punkt = punkte_class(bot)
    await punkt.remove_user(user)
    await ctx.respond(f"{user.mention} wurde entfernt.", ephemeral=True)

@remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("Nur Admins dürfen diesen Befehl nutzen ❌", ephemeral=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != 'check_questions.py':
        bot.load_extension(f'cogs.{filename[:-3]}')
#bot.load_extension('cogs.duel_requests')

bot.choosen_kategories = string_of_kategories
bot.choosen_difficulties = string_of_difficulties
bot.anzahlfragen = anzahlfragen
bot.invitelink = invitelink
bot.send_message_allowed = send_message_allowed

@bot.event
async def on_ready():
    await bot.sync_commands()
    print(f"Eingeloggt als {bot.user}")

bot.run(Token)
