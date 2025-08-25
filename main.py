import discord as dc # type: ignore
from discord.ext import commands # type: ignore
from discord.ui import Button # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import asyncio
from cogs import database, duel_requests


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

class Dropdown_Kategorie(dc.ui.Select):
    
    def __init__(self, user: dc.Member, author: dc.Member):
        global _disabled
        options = [
            dc.SelectOption(label="Alles", value="any"),
            dc.SelectOption(label="Allgemeinwissen", value="Allgemeinwissen"),
            dc.SelectOption(label="Geschichte", value="Geschichte"),
            dc.SelectOption(label="Geographie", value="Geographie"),
            dc.SelectOption(label="Mathematik", value="Mathematik"),
            dc.SelectOption(label="Literatur", value="Literatur"),
            dc.SelectOption(label="Moderne", value="Moderne"),
            dc.SelectOption(label="Wissenschaft", value="Wissenschaft"),
            dc.SelectOption(label="Technologie", value="Technologie"),
        ]
        super().__init__(placeholder="Wähle das Thema:", options=options, min_values=1, max_values=8, disabled=_disabled)
        self.user = user
        self.author = author

    async def callback(self, interaction: dc.Interaction):
        global string
        global string_list
        global list_of_kategories
        global string_of_kategories

        if "any" in self.values:
            string = "Allgemeinwissen, Geschichte, Geographie, Mathe, Literatur, Moderne, Wissenschaft, Technologie"
            list_of_kategories = ["Allgemeinwissen", "Geschichte", "Geographie", "Mathematik", "Literatur", "Moderne", "Wissenschaft", "Technologie"]
        else:
            for value in self.values:
                if value == "Allgemeinwissen":
                    string_list.append("Allgemeinwissen, ")
                    list_of_kategories.append("'Allgemeinwissen', ")

                elif value == "Geschichte":
                    string_list.append("Geschichte, ")
                    list_of_kategories.append("'Geschichte', ")

                elif value == "Geographie":
                    string_list.append("Geographie, ")
                    list_of_kategories.append("'Geographie', ")

                elif value == "Mathematik":
                    string_list.append("Mathematik, ")
                    list_of_kategories.append("'Mathematik', ")

                elif value == "Literatur":
                    string_list.append("Literatur, ")
                    list_of_kategories.append("'Literatur', ")

                elif value == "Moderne":
                    string_list.append("Moderne, ")
                    list_of_kategories.append("'Moderne', ")

                elif value == "Wissenschaft":
                    string_list.append("Wissenschaft, ")
                    list_of_kategories.append("'Wissenschaft', ")

                elif value == "Technologie":
                    string_list.append("Technologie, ")
                    list_of_kategories.append("'Technologie', ")

            string = "".join(string_list)
            string = string[:-2] 
            string_of_kategories = "".join(list_of_kategories)
            string_of_kategories = string_of_kategories[:-2]
        await interaction.response.defer() 
       # embed_callback = dc.Embed(title="Themenfeld ausgewählt", description=f"{self.user.mention} hat {string} als Themenfeld ausgewählt.\n {self.author.mention}", color=0x0099E1)
        #await interaction.response.send_message(embed=embed_callback)


class Dropdown_Schwierigkeit(dc.ui.Select):
    def __init__(self, user: dc.Member, author: dc.Member):
        global _disabled
        options = [
            dc.SelectOption(label="Einfach", value="leicht"),
            dc.SelectOption(label="Normal", value="mittel"),
            dc.SelectOption(label="Schwer", value="schwer"),
        ]
        super().__init__(placeholder="Wähle die Schwierigkeit:", options=options, min_values=1, max_values=3, disabled=_disabled)
        self.user = user
        self.author = author

    async def callback(self, interaction: dc.Interaction):
        global string1
        global string1_list
        global list_of_difficulties
        global string_of_difficulties
        
        for value in self.values:
                if value == "leicht":
                    string1_list.append("Leicht, ")
                    list_of_difficulties.append("'EASY', ")

                elif value == "mittel":
                    string1_list.append("Normal, ")
                    list_of_difficulties.append("'MEDIUM', ")

                elif value == "schwer":
                    string1_list.append("Schwer, ")
                    list_of_difficulties.append("'HARD', ")

        string1 = "".join(string1_list)
        string1 = string1[:-2]
        string_of_difficulties = "".join(list_of_difficulties)
        string_of_difficulties = string_of_difficulties[:-2]
        await interaction.response.defer() 
        #await interaction.response.send_message(f"{self.user.mention} hat {string1} als Schwierigkeit ausgewählt.\n {self.author.mention}")

class Dropdown_Anzahl_Fragen(dc.ui.Select):
    def __init__(self, user: dc.Member, author: dc.Member):
        global _disabled
        options = [
            dc.SelectOption(label=str(i), value=str(i)) for i in range(1, 26)
            ]
        
        super().__init__(placeholder="Wähle die Anzahl der Fragen:", options=options, min_values=1, max_values=1, disabled=_disabled)
        self.user = user
        self.author = author

    async def callback(self, interaction: dc.Interaction):
        global anzahlfragen
        anzahlfragen = int(self.values[0])
        await interaction.response.defer() 
       # await interaction.response.send_message(f"{self.user.mention} hat {self.values[0]} als Anzahl der Fragen ausgewählt.\n {self.author.mention}")

class Quiz_create_View(dc.ui.View):

    def __init__(self, user: dc.Member, author: dc.Member):
        super().__init__(timeout=300)
        self.user = user
        self.author = author
        self.message = None
        self.add_item(Dropdown_Kategorie(user, author))
        self.add_item(Dropdown_Schwierigkeit(user, author)) 
        self.add_item(Dropdown_Anzahl_Fragen(user, author))
    
    async def on_timeout(self):
        self.disable_all_items()
        if self.message:

            embed_timeout = dc.Embed(title="🕒 Quiz Erstellung abgelaufen", description = f"Die Zeit, zum erstellen des Quizes ist abgelaufen, bitte startet das Quiz erneut.\n {self.user.mention} {self.author.mention}", color = 0x0099E1)

            await self.message.edit(view=self)
            await self.message.channel.send(embed=embed_timeout, view=self)

    @dc.ui.button(label="Quiz starten", style=dc.ButtonStyle.green)
    async def button_start_quiz_callback(self, button, interaction):
        global string
        global string1
        global anzahlfragen
        global _disabled
        _disabled = True
        self.disable_all_items()
        await self.message.edit(view=self)
        embed_start = dc.Embed(title="Quiz gestartet", description=f"Das Quiz wird in 10s mit {self.user.mention} und {self.author.mention} gestartet.\n\n **Schwierigkeit**\n{self.author.mention} hat {string1} als Schwierigkeit ausgewählt. \n\n **Themenbereich**\n{self.author.mention} hat {string} als Themenbereich ausgewählt.\n\n **Fragenanzahl** \n {self.author.mention} hat {anzahlfragen} als Fragenanzahl ausgewählt\n", color=0x00D166)
        await interaction.response.send_message(embed=embed_start)
        self.stop()


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



@bot.slash_command()
async def duel(msg, user: dc.Member):
    
    duel_requests.duel_request(msg, user)

async def make_channel(author: dc.Member, user: dc.Member, angenommen): 
        global invitelink
        global inviteguild
        global invite_channel

        overwrites = {
            inviteguild.default_role: dc.PermissionOverwrite(view_channel=False),  
            author: dc.PermissionOverwrite(view_channel=True),
            user: dc.PermissionOverwrite(view_channel=True) 
            }
            
        await create_quiz_channel(inviteguild, user, author, overwrites = overwrites) 

        embed_invite = dc.Embed(title = "Joine dem Quizkanal", description = f"{invitelink}\n", color = 0x0099E1)  

        embed_create_quiz = dc.Embed(title = "Erstelle ein Quiz", description = f"** {author.mention} stelle dein Quiz zusammen und starte es!**\n\n Bitte wähle die Anzahl an Fragen, den Themenbereich \nund die Schwierigkeit des Quizes aus.\n", color = 0x0099E1)

        embed_create_quiz.set_author(name=author.display_name, icon_url=author.avatar.url)
        await author.send(embed =embed_invite)
        await user.send(embed =embed_invite)

        view = Quiz_create_View(user, author)

        await invite_channel.send(embed = embed_create_quiz, view = view)

        while not view.is_finished():
                await asyncio.sleep(1)
            
            
        fragen = await database.find_questions()
        if fragen:
            for frage in fragen:
                    
                question_embed = dc.Embed(title=frage[1], description="Bitte gebt sendet eure Antworten ein.\n Ihr habt **3 Minuten** zeit die Frage zu beantworten", color=0x0099E1)
                await invite_channel.send(embed=question_embed)
                modal_player_user = Quiz_Modal(user, frage[1], frage[2], title="Quiz Antwort")
                modal_player_author = Quiz_Modal(author, frage[1], frage[2], title="Quiz Antwort")

                await invite_channel.send_modal(modal=modal_player_user)
                await invite_channel.send_modal(modal=modal_player_author)
        else:
            await invite_channel.send("Keine Fragen für das quiz gefunden.")

async def create_quiz_channel(guild : dc.Guild, user : dc.Member, author : dc.Member, overwrites = None):
    global invitelink
    global invite_channel

    channel = await guild.create_text_channel(f" Quiz Kanal {user.mention}{author.mention}", overwrites=overwrites)
    invitelink = await channel.create_invite(max_uses = 2, unique = True)
    invite_channel = channel

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.choosen_kategories = string_of_kategories
bot.choosen_difficulties = string_of_difficulties
bot.anzahlfragen = anzahlfragen
bot.invitelink = invitelink
bot.inviteguild = inviteguild
bot.invite_channel = invite_channel

bot.run(Token)
