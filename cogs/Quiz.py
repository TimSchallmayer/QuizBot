import discord as dc
from discord.ext import commands
import asyncio
from cogs.check_questions import check_questions as check_questions_class
from cogs.database_punkte import Punkte as punkte_class


class Quiz(commands.Cog):
    
    def __init__(self, bot, fragen, user : dc.Member, author : dc.Member):
        from cogs.make_channel import make_channel as make_channel_class
        
        self.bot = bot
        self.fragen = fragen
        self.user = user
        self.author = author    
        self.make_channel_class = make_channel_class(self.bot)

    async def quiz(self):
        fragen = self.fragen
        user = self.user
        author = self.author
        self.bot.points_user = 0
        self.bot.points_author = 0
        if fragen:
            for frage in fragen:   
                global string_dificulty 
                string_dificulty = "" 
                if frage[3] == "EASY":
                    string_dificulty = "Einfach"
                if frage[3] == "MEDIUM":
                    string_dificulty = "Normal"
                if frage[3] == "HARD":
                    string_dificulty = "Schwer"  
                question_embed = dc.Embed(title=frage[1], description=f"Schwierigkeit: {string_dificulty} \n Kategorie: {frage[4]}\n\nBitte gebt sendet eure Antworten ein.\n", color=0x0099E1)
                view_skip = Quiz_skip_View(self.bot, frage, user, author)
                await self.bot.invite_channel.send(embed=question_embed, view=view_skip) 
                
                if self.bot.get_cog("check_questions"):
                    self.bot.remove_cog("check_questions")

                check_question_cog = check_questions_class(self.bot, frage[2], self.bot.invite_channel, user, author, frage[3])
                self.bot.add_cog(check_question_cog)

                self.bot.send_message_allowed = True

                while self.bot.send_message_allowed and not view_skip.is_finished():
                    await asyncio.sleep(1)

                self.bot.send_message_allowed = False
                self.bot.remove_cog("check_questions")
                view_skip.stop()

                await asyncio.sleep(2)
                continue
            view_end = Quiz_restart_View(self.bot, user, author, self.make_channel_class)
            if self.bot.points_author > self.bot.points_user:
                    winner_string = f"{author.name} hat gewonnen 🎉!"
            elif self.bot.points_author < self.bot.points_user:
                winner_string = f"{user.name} hat gewonnen 🎉!"
            else:
                winner_string = "Unentschieden!"

            embed_end = dc.Embed(title=f"{winner_string}", description=f"Das Quiz ist nun beendet. Vielen Dank fürs Mitmachen {author.mention} und {user.mention}!\n\nIhr könnt den Kanal nun verlassen oder ein neues Quiz starten.\nDieser Kanal wird in 2 Minuten gelöscht", color=0x0099E1)
            await self.bot.invite_channel.send(embed=embed_end, view = view_end)

            punkte = punkte_class(self.bot)
            if await punkte.does_user_exist(author) == False:
                if self.bot.points_author > self.bot.points_user:
                    await punkte.add_user(author, self.bot.points_author, 1, 0, 0)
                elif self.bot.points_author < self.bot.points_user:
                    await punkte.add_user(author, self.bot.points_author, 0, 1, 0)
                else:
                    await punkte.add_user(author, self.bot.points_author, 0, 0, 1)
            else:
                if self.bot.points_author > self.bot.points_user:
                    await punkte.update_user(author, self.bot.points_author, 1, 0, 0)
                elif self.bot.points_author < self.bot.points_user:
                    await punkte.update_user(author, self.bot.points_author, 0, 1, 0)
                else:
                    await punkte.update_user(author, self.bot.points_author, 0, 0, 1)

            if await punkte.does_user_exist(user) == False:
                if self.bot.points_user > self.bot.points_author:
                    await punkte.add_user(user, self.bot.points_user, 1, 0, 0)
                elif self.bot.points_user < self.bot.points_author:
                    await punkte.add_user(user, self.bot.points_user, 0, 1, 0)
                else:
                    await punkte.add_user(user, self.bot.points_user, 0, 0, 1)

            else:
                if self.bot.points_user > self.bot.points_author:
                    await punkte.update_user(user, self.bot.points_user, 1, 0, 0)
                elif self.bot.points_user < self.bot.points_author:
                    await punkte.update_user(user, self.bot.points_user, 0, 1, 0)
                else:
                    await punkte.update_user(user, self.bot.points_user, 0, 0, 1)

        else:

            view_end = Quiz_restart_View(self.bot, user, author, self.make_channel_class)
            embed_1 = dc.Embed(title="Keine Fragen gefunden", description="Es wurden keine Fragen gefunden, die den ausgewählten Kriterien entsprechen. Bitte startet das Quiz erneut und wählt andere Kriterien aus.\n", color=0xF93A2F)
            await self.bot.invite_channel.send(embed=embed_1, view = view_end)


class Quiz_restart_View(dc.ui.View):
    def __init__(self, bot, user : dc.Member, author : dc.Member, make_channel):
        super().__init__(timeout=120)
        self.bot = bot
        self.user = user
        self.author = author
        self.make_channel = make_channel
        self.old_channel = self.bot.invite_channel
    

    async def on_timeout(self):
        self.disable_all_items()
        try:
            await self.message.edit(view=self)
        except dc.NotFound:
            return
        await self.old_channel.delete()
        self.stop()

    @dc.ui.button(label="Neues Quiz starten", style=dc.ButtonStyle.green)
    async def button_restart_quiz_callback(self, button, interaction : dc.Interaction):
        await interaction.response.defer()
        self.bot.send_message_allowed = False
        await self.make_channel.make_channel_def(self.author, self.user, 1, self.bot.invite_channel)
        self.disable_all_items()
        await interaction.edit_original_response(view=self)
        await self.old_channel.delete()
        self.stop()


class Quiz_skip_View(dc.ui.View):
    def __init__(self, bot, frage, user : dc.Member, author : dc.Member):
        super().__init__(timeout=None)
        self.bot = bot
        self.frage = frage
        self.user = user
        self.author = author

    @dc.ui.button(label="Frage überspringen", style=dc.ButtonStyle.blurple)
    async def button_skip_question_callback(self, button, interaction):
        self.bot.send_message_allowed = False
        embed_skip = dc.Embed(title="Frage übersprungen", description=f"Die Frage wird übersprungen.\n Die Richtige Antwort lautet: {self.frage[2]}\n\n **Aktueller Punktestand**\n {self.author.mention}:  {self.bot.points_author} \n {self.user.mention}: {self.bot.points_user} \n", color=0xF93A2F)
        await interaction.response.send_message(embed=embed_skip)
        self.disable_all_items()
        await interaction.message.edit(view=self)
        self.stop()


async def setup(bot):
    await bot.add_cog(Quiz(bot))