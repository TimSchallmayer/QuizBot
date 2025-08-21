import discord as dc # type: ignore
from discord.ext import commands # type: ignore
from discord.ui import Button # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import asyncio
import mysql.connector # type: ignore


db = mysql.connector.connect(
    host = "localhost",
    port = 3000,
    user = "root",
    password = "root",
    database = "main"
)

cursor = db.cursor()


invitelink = None
inviteguild = None

load_dotenv()
Token = os.getenv("DISCORD_BOT_TOKEN")

intents = dc.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents
)

class Anfrage_View(dc.ui.View): 

    def __init__(self, msg, user: dc.Member): 
        super().__init__(timeout=120)
        self.message = None
        self.msg = msg
        self.user = user
        self.completed = False

    async def on_timeout(self):
        if self.completed:
            return
        self.disable_all_items()
        embed_timeout = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {self.msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x597E8D)
        embed_timeout.set_author(name=self.msg.author.display_name, icon_url=self.msg.author.avatar.url)
        await self.message.edit(embed=embed_timeout, view = self)
        await self.user.send(f"🕒 Die Zeit ist abgelaufen {self.user.mention}, falls du doch spielen willst schicke eine neue Anfrage!", reference = self.message)
        await response(self.msg.author, self.user, 2)
        

    @dc.ui.button(label="Akzeptieren", style = dc.ButtonStyle.green)
    async def button_accept_callback(self, button, interaction):
        self.completed = True
        self.disable_all_items()
        await interaction.response.send_message("🎉 Du hast das Quiz akzeptiert!")
        await self.message.edit(view=self)
        await response(self.msg.author, interaction.user, 0)
        self.stop()
    
    @dc.ui.button(label="Ablehnen", style = dc.ButtonStyle.red)
    async def button_reject_callback(self, button, interaction):

        self.disable_all_items()
        await interaction.response.send_message("❌ Du hast das Quiz abgelehnt!")
        await self.message.edit(view=self)
        await response(self.msg.author, interaction.user, 1)
        self.stop()
class Auswahl_View(dc.ui.View):
    def __init__(self, user: dc.Member):
        self.user = user

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
@bot.slash_command()
async def duel(msg, user: dc.Member):
    global inviteguild

    embed_succesfull = dc.Embed(title = "Anfrage wurde verschickt", description = f"Eine Quiz Anfrage wurde an {user.mention} gesendet.\n", color = 0x00D166)
    embed_succesfull.set_author(name = user.display_name, icon_url = user.avatar.url)

    embed_error = dc.Embed(title = "Anfrage wurde nicht zugestellt", description = f"{user.mention} konnte nicht gefunden werden oder akzeptiert keien Dms.", color = 0xF93A2F)
    embed_error.set_author(name = user.display_name, icon_url = user.avatar.url)
    
    
    try:
        # await msg.author.send(embed = embed_succesfull)
        await msg.response.send_message(embed = embed_succesfull, ephemeral=True)
        
        

        embed = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x0099E1)
        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)

        view = Anfrage_View(msg, user)
        try:
            sent_message = await user.send(embed=embed, view=view)
        except dc.Forbidden:
            msg.author.send("Der Nutzer ist nicht erreichbar, da er vermutlich keine Dms akzeptiert.")
            return
        view.message = sent_message
        inviteguild = msg.channel.guild
        await view.wait()

    except dc.Forbidden:
        await msg.author.send(embed = embed_error)

async def response(author: dc.Member, user: dc.Member, angenommen): 
        global invitelink
        global inviteguild
        global invite_channel
        
        embed_reject = dc.Embed(title = "❌ Anfrage abgelehnt ❌", description = (f"{user.mention} hat die Anfrage abgelehnt.\n"), color = 0xF93A2F)
        embed_reject.set_author(name=user.display_name, icon_url= user.avatar.url)

        embed_accept = dc.Embed(title= "✅ Anfrage angenommen ✅", description = (f"{user.mention} hat die Anfrage angenommen.\n"), color = 0x00D166)
        embed_accept.set_author(name=user.display_name, icon_url = user.avatar.url)

        embed_timeout = dc.Embed(title = "🕒 Nicht auf Anfrage reagiert (Timeout) 🕒", description = (f"{user.mention} hat nicht auf die Anfrage reagiert (Timeout).\n" "Versuche die Anfrage erneut zu senden \noder den Nutzer anders zu erreichen\n"), color = 0x597E8D)
        embed_timeout.set_author(name = user.display_name, icon_url = user.avatar.url)

        

        if angenommen == 0:
            await author.send(embed = embed_accept)

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
                
            await find_questions()
            
        elif angenommen == 1: 
            await author.send(embed = embed_reject)  
        else:
            await author.send(embed = embed_timeout)  

async def create_quiz_channel(guild : dc.Guild, user : dc.Member, author : dc.Member, overwrites = None):
    global invitelink
    global invite_channel

    channel = await guild.create_text_channel(f" Quiz Kanal {user.mention}{author.mention}", overwrites=overwrites)
    invitelink = await channel.create_invite(max_uses = 2, unique = True)
    invite_channel = channel

async def find_questions():
    global string_of_kategories
    global string_of_difficulties
    global anzahlfragen

    sql_query = f"""SELECT * FROM FRAGEN 
            WHERE KATERGORIE IN ({string_of_kategories}) AND DIFFICULTY IN ({string_of_difficulties}) 
            ORDER BY RAND();"""

    cursor.execute(sql_query)

    rows = cursor.fetchmany(anzahlfragen)

    for row in rows:
        print(row)


bot.run(Token)
