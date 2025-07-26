import discord as dc # type: ignore
from discord.ext import commands # type: ignore
from discord.ui import Button # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import asyncio
import mysql.connector # type: ignore


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "2606009",
    database = "sys"
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

    async def on_timeout(self):
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
        
        self.disable_all_items()
        await interaction.response.send_message("🎉 Du hast das Quiz akzeptiert!")
        await self.message.edit(view=self)
        await response(interaction.author, interaction.user, 0)
        self.stop()
    
    @dc.ui.button(label="Ablehnen", style = dc.ButtonStyle.red)
    async def button_reject_callback(self, button, interaction):

        self.disable_all_items()
        await interaction.response.send_message("❌ Du hast das Quiz abgelehnt!")
        await self.message.edit(view=self)
        await response(interaction.author, interaction.user, 1)
        self.stop()

class Auswahl_View(dc.ui.View):
    def __init__(self, user: dc.Member):
        self.user = user
    


class Dropdown_Kategorie(dc.ui.Select):

    def __init__(self, user: dc.Member):
        options = [
            dc.SelectOption(label="Alles", value="any"),
            dc.SelectOption(label="Allgemeinwissen", value="allgemein"),
            dc.SelectOption(label="Geschichte", value="geschichte"),
            dc.SelectOption(label="Geographie", value="geographie"),
            dc.SelectOption(label="Mathematik", value="mathe"),
            dc.SelectOption(label="Literatur", value="literatur"),
            dc.SelectOption(label="Moderne", value="moderne"),
            dc.SelectOption(label="Wissenschaft", value="wissenschaft"),
            dc.SelectOption(label="Technologie", value="technologie"),
        ]
        super().__init__(placeholder="Wähle das Thema:", options=options)
        self.user = user

    async def callback(self, interaction: dc.Interaction):
        if self.values[0] == "any":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Alles ausgewählt.")
        elif self.values[0] == "allgemein":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Allgemeinwissen ausgewählt.")
        elif self.values[0] == "geschichte":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Geschichte ausgewählt.")
        elif self.values[0] == "geographie":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Geographie ausgewählt.")
        elif self.values[0] == "mathe":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Mathematik ausgewählt.")
        elif self.values[0] == "literatur":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Literatur ausgewählt.")
        elif self.values[0] == "moderne":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Moderne ausgewählt.")
        elif self.values[0] == "wissenschaft":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Wissenschaft ausgewählt.")
        elif self.values[0] == "technologie":
            await interaction.response.send_message(f"{self.user.mention} hat die Kategorie Technologie ausgewählt.")


class Dropdown_Schwierigkeit(dc.ui.Select):
    def __init__(self, user: dc.Member):
        options = [
            dc.SelectOption(label="Einfach", value="leicht"),
            dc.SelectOption(label="Normal", value="mittel"),
            dc.SelectOption(label="Schwer", value="schwer"),
            dc.SelectOption(label="Alle", value="alle"),
            dc.SelectOption(label="Einfach und Normal", value="einfach_mittel"),
            dc.SelectOption(label="Normal und Schwer", value="normal_schwer"),
        ]
        super().__init__(placeholder="Wähle die Schwierigkeit:", options=options)
        self.user = user

    async def callback(self, interaction: dc.Interaction):
        if self.values[0] == "leicht":
            await interaction.response.send_message(f"{self.user.mention} hat die Schwierigkeit Einfach ausgewählt.")
        elif self.values[0] == "mittel":
            await interaction.response.send_message(f"{self.user.mention} hat die Schwierigkeit Normal ausgewählt.")
        elif self.values[0] == "schwer":
            await interaction.response.send_message(f"{self.user.mention} hat die Schwierigkeit Schwer ausgewählt.")
        elif self.values[0] == "alle":
            await interaction.response.send_message(f"{self.user.mention} hat jede Schwierigkeit ausgewählt.")
        elif self.values[0] == "einfach_mittel":
            await interaction.response.send_message(f"{self.user.mention} hat die Schwierigkeit Einfach und Normal ausgewählt.")
        elif self.values[0] == "normal_schwer":
            await interaction.response.send_message(f"{self.user.mention} hat die Schwierigkeit Normal und Schwer ausgewählt.")

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
        
        embed_reject = dc.Embed(title = "❌ Anfrage abgelehnt ❌", description = (f"{user.mention} hat die Anfrage abgelehnt.\n"), color = 0xF93A2F)
        embed_reject.set_author(name=user.display_name, icon_url= user.avatar.url)

        embed_accept = dc.Embed(title= "✅ Anfrage angenommen ✅", description = (f"{user.mention} hat die Anfrage angenommen.\n"), color = 0x00D166)
        embed_accept.set_author(name=user.display_name, icon_url = user.avatar.url)

        embed_timeout = dc.Embed(title = "🕒 Nicht auf Anfrage reagiert (Timeout) 🕒", description = (f"{user.mention} hat nicht auf die Anfrage reagiert (Timeout).\n" "Versuche die Anfrage erneut zu senden \noder den Nutzer anders zu erreichen\n"), color = 0x597E8D)
        embed_timeout.set_author(name = user.display_name, icon_url = user.avatar.url)

        

        if angenommen == 0:
            await author.send(embed = embed_accept)
            await create_quiz_channel(inviteguild, user, author) 
            embed_invite = dc.Embed(title = "Joine dem Quizkanal", description = f"{invitelink}\n", color = 0x0099E1)  
            await author.send(embed =embed_invite)
            await user.send(embed =embed_invite)
        elif angenommen == 1: 
            await author.send(embed = embed_reject)  
        else:
            await author.send(embed = embed_timeout)  

async def create_quiz_channel(guild : dc.Guild, user : dc.Member, author : dc.Member):
    global invitelink

    channel = await guild.create_text_channel(f" Quiz Kanal {user.mention}{author.mention}")
    invitelink = await channel.create_invite(max_uses = 2, unique = True)

bot.run(Token)
