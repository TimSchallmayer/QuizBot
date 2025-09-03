import discord as dc
from discord.ext import commands
from cogs.database import Database as database_class
from cogs.Quiz import Quiz as quiz_class
import asyncio
from cogs.check_questions import check_questions as check_questions_class



class make_channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def make_channel_def(self, author: dc.Member, user: dc.Member, which_way, channel): 


        overwrites = {
            self.bot.inviteguild.default_role: dc.PermissionOverwrite(view_channel=False),  
            author: dc.PermissionOverwrite(view_channel=True, send_messages= True, read_messages=True),
            user: dc.PermissionOverwrite(view_channel=True, send_messages= True, read_messages=True) 

            }
            
        await create_quiz_channel(self, self.bot.inviteguild, user, author, overwrites = overwrites) 

        embed_invite = dc.Embed(title = "Joine dem Quizkanal", description = f"[Klicke hier um beizutreten]({self.bot.invitelink})\n", color = 0x0099E1)  

        embed_create_quiz = dc.Embed(title = "Erstellt ein Quiz", description = f"** {author.mention} {user.mention} stellt euer Quiz zusammen und startet es!**\n\n Bitte wählt die Anzahl an Fragen, den Themenbereich \nund die Schwierigkeit des Quizes aus.\n", color = 0x0099E1)
        if which_way == 0:
            await author.send(embed =embed_invite)
            await user.send(embed =embed_invite)
        else:
            await channel.send(embed=embed_invite)
        if self.bot.get_cog("check_questions"):
                    self.bot.remove_cog("check_questions")

        check_question_cog = check_questions_class(self.bot, "", self.bot.invite_channel, user, author, "")
        self.bot.add_cog(check_question_cog)
                    
        view = Quiz_create_View(user, author, self.bot)
        self.bot.send_messages_allowed = False
        await self.bot.invite_channel.send(embed = embed_create_quiz, view = view)

        while not view.is_finished() and self.bot.success == False:
                await asyncio.sleep(1)
        
        database = database_class(self.bot)
        fragen = await database.find_questions()
        self.bot.choosen_kategories = ""
        self.bot.choosen_difficulties = ""
        self.bot.anzahlfragen = 0

        quiz_class_variable = quiz_class(self.bot, fragen, user, author, )
        await quiz_class_variable.quiz()

        self.bot.remove_cog("check_questions")


async def create_quiz_channel(self, guild : dc.Guild, user : dc.Member, author : dc.Member, overwrites = None):

    channel = await guild.create_text_channel(f" Quiz Kanal {user.mention}{author.mention}", overwrites=overwrites)
    link = await channel.create_invite(max_uses = 2, unique = True)
    self.bot.invitelink = link.url
    invite_channel = channel
    self.bot.invite_channel = invite_channel


class Dropdown_Kategorie(dc.ui.Select):
    
    def __init__(self, user: dc.Member, author: dc.Member, bot):
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
        super().__init__(placeholder="Wähle das Thema:", options=options, min_values=1, max_values=8)
        self.user = user
        self.author = author
        self.bot = bot

    async def callback(self, interaction: dc.Interaction):
        string = ""
        string_list = []
        list_of_kategories = []
        string_of_kategories = ""

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
            self.bot.string_of_kategories = string
            self.bot.choosen_kategories = string_of_kategories
        await interaction.response.defer() 
       # embed_callback = dc.Embed(title="Themenfeld ausgewählt", description=f"{self.user.mention} hat {string} als Themenfeld ausgewählt.\n {self.author.mention}", color=0x0099E1)
        #await interaction.response.send_message(embed=embed_callback)
        self.values.clear() 

class Dropdown_Schwierigkeit(dc.ui.Select):
    def __init__(self, user: dc.Member, author: dc.Member, bot):
        global _disabled
        options = [
            dc.SelectOption(label="Einfach", value="leicht"),
            dc.SelectOption(label="Normal", value="mittel"),
            dc.SelectOption(label="Schwer", value="schwer"),
        ]
        super().__init__(placeholder="Wähle die Schwierigkeit:", options=options, min_values=1, max_values=3)
        self.user = user
        self.author = author
        self.bot = bot

    async def callback(self, interaction: dc.Interaction):
        string_of_difficulties = ""
        list_of_difficulties = []
        string1 = ""
        string1_list = []
        
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
        self.bot.string_of_difficulties = string1
        self.bot.choosen_difficulties = string_of_difficulties
        await interaction.response.defer() 
        #await interaction.response.send_message(f"{self.user.mention} hat {string1} als Schwierigkeit ausgewählt.\n {self.author.mention}")
        self.values.clear() 

class Dropdown_Anzahl_Fragen(dc.ui.Select):
    def __init__(self, user: dc.Member, author: dc.Member, bot):
        global _disabled
        options = [
            dc.SelectOption(label=str(i), value=str(i)) for i in range(1, 26)
            ]
        
        super().__init__(placeholder="Wähle die Anzahl der Fragen:", options=options, min_values=1, max_values=1)
        self.user = user
        self.author = author
        self.bot = bot

    async def callback(self, interaction: dc.Interaction):      
        anzahlfragen = 0
        anzahlfragen = int(self.values[0])
        self.bot.anzahlfragen = anzahlfragen
        await interaction.response.defer() 
       # await interaction.response.send_message(f"{self.user.mention} hat {self.values[0]} als Anzahl der Fragen ausgewählt.\n {self.author.mention}")
        self.values.clear() 

class Quiz_create_View(dc.ui.View):

    def __init__(self, user: dc.Member, author: dc.Member, bot):
        super().__init__(timeout=300)
        self.user = user
        self.author = author
        self.message = None
        self.bot = bot
        self.channel = self.bot.invite_channel
        self.add_item(Dropdown_Kategorie(user, author, self.bot))
        self.add_item(Dropdown_Schwierigkeit(user, author, self.bot)) 
        self.add_item(Dropdown_Anzahl_Fragen(user, author, self.bot))
        self.bot.success = False
    async def on_timeout(self):
        self.disable_all_items()
        if self.message:

            embed_timeout = dc.Embed(title="🕒 Quiz Erstellung abgelaufen", description = f"Die Zeit, zum erstellen des Quizes ist abgelaufen, bitte startet das Quiz erneut.\n {self.user.mention} {self.author.mention}", color = 0x0099E1)

            await self.message.edit(view=self)
            await self.message.channel.send(embed=embed_timeout)
        
        await asyncio.sleep(10)
        await self.channel.delete()

    @dc.ui.button(label="Quiz starten", style=dc.ButtonStyle.green)
    async def button_start_quiz_callback(self, button, interaction):
        global string
        global string1
        global anzahlfragen
        global _disabled
        _disabled = True
        
        if self.bot.anzahlfragen != 0 and self.bot.choosen_kategories != "" and self.bot.choosen_difficulties != "":
            self.disable_all_items()
            newembed = dc.Embed(title = "Erstelle ein Quiz", description = f"{self.author.mention} und {self.user.mention} stellt euer Quiz zusammen und startet es!\n\n**Schwierigkeit**\n Ihr habt {self.bot.string_of_difficulties} als Schwierigkeit ausgewählt. \n\n **Themenbereich**\n Ihr habt {self.bot.string_of_kategories} als Themenbereich ausgewählt.\n\n **Fragenanzahl** \n Ihr habt {self.bot.anzahlfragen} als Fragenanzahl ausgewählt\n", color = 0x00D166)
            await self.message.edit(embed=newembed ,view=self)
            embed_start = dc.Embed(title="Quiz gestartet", description=f"Das Quiz wird in ein paar Sekunden mit {self.user.mention} und {self.author.mention} gestartet.\n\n **Regeln**\n Wer als erstes auf die gestellte Frage antwortet gewinnt.", color=0x00D166)
            await interaction.response.send_message(embed=embed_start)
            self.bot.success = True
            self.stop()
           
        else:
            embed_not_complete = dc.Embed(title="❌ Quiz nicht gestartet ❌", description=f"{self.user.mention} und {self.author.mention} bitte wählt alle Optionen aus, bevor ihr das Quiz startet!\n", color=0xF93A2F)
            await interaction.response.send_message(embed = embed_not_complete)

async def setup(bot):
    await bot.add_cog(make_channel(bot))