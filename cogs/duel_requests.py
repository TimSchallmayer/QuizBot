import discord as dc
from discord.ext import commands
from cogs.make_channel import make_channel as make_channel_class


class duel_requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    async def duel_request(self, msg, user: dc.Member):
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

            view = Anfrage_View(msg, user, self.bot)
            try:
                sent_message = await user.send(embed=embed, view=view)
            except dc.Forbidden:
                msg.author.send("Der Nutzer ist nicht erreichbar, da er vermutlich keine Dms akzeptiert.")
                return
            view.message = sent_message
            self.bot.inviteguild = msg.channel.guild
            await view.wait()

        except dc.Forbidden:
            await msg.author.send(embed = embed_error)

class Anfrage_View(dc.ui.View): 

    def __init__(self, msg, user: dc.Member, bot): 
        super().__init__(timeout=120)
        self.message = None
        self.msg = msg
        self.user = user
        self.completed = False
        self.bot = bot

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
        await response(self.bot, self.msg.author, self.user, 2)
        

    @dc.ui.button(label="Akzeptieren", style = dc.ButtonStyle.green)
    async def button_accept_callback(self, button, interaction):
        self.completed = True
        self.disable_all_items()
        await interaction.response.send_message("🎉 Du hast das Quiz akzeptiert!")
        await self.message.edit(view=self)
        await response(self.bot, self.msg.author, self.user, 0)
        self.stop()
    
    @dc.ui.button(label="Ablehnen", style = dc.ButtonStyle.red)
    async def button_reject_callback(self, button, interaction):

        self.disable_all_items()
        await interaction.response.send_message("❌ Du hast das Quiz abgelehnt!")
        await self.message.edit(view=self)
        await response(self.bot, self.msg.author, self.user, 1)
        self.stop()

async def response(bot, author: dc.Member, user: dc.Member, angenommen): 
        
        embed_reject = dc.Embed(title = "❌ Anfrage abgelehnt ❌", description = (f"{user.mention} hat die Anfrage abgelehnt.\n"), color = 0xF93A2F)
        embed_reject.set_author(name=user.display_name, icon_url= user.avatar.url)

        embed_accept = dc.Embed(title= "✅ Anfrage angenommen ✅", description = (f"{user.mention} hat die Anfrage angenommen.\n"), color = 0x00D166)
        embed_accept.set_author(name=user.display_name, icon_url = user.avatar.url)

        embed_timeout = dc.Embed(title = "🕒 Nicht auf Anfrage reagiert (Timeout) 🕒", description = (f"{user.mention} hat nicht auf die Anfrage reagiert (Timeout).\n" "Versuche die Anfrage erneut zu senden \noder den Nutzer anders zu erreichen\n"), color = 0x597E8D)
        embed_timeout.set_author(name = user.display_name, icon_url = user.avatar.url)

        

        if angenommen == 0:
            await author.send(embed = embed_accept)
            channel = None
            class_of_make_channel = make_channel_class(bot)
            await class_of_make_channel.make_channel_def(author, user, 0, channel)  
            return
            
        elif angenommen == 1: 
            await author.send(embed = embed_reject)  
            return

        else:
            await author.send(embed = embed_timeout)  
            return



async def setup(bot):
    await bot.add_cog(duel_requests(bot))