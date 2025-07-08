import discord as dc # type: ignore
from discord.ext import commands # type: ignore
from discord.ui import Button # type: ignore
import requests # type: ignore
import json
import time
import os
from dotenv import load_dotenv # type: ignore
import asyncio

load_dotenv()
Token = os.getenv("DISCORD_BOT_TOKEN")

intents = dc.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents
)


@bot.command()
async def duel(msg, user: dc.Member):
    try:
        await msg.send(f"Hi{user.mention}, die Anfrage wurde gesendet", ephemeral = True)
        class Myview(dc.ui.View): 

            def __init__(self): 
                super().__init__(timeout=120)
                self.message = None

            async def on_timeout(self):
                self.disable_all_items()
                await self.message.edit(embed=embed_timeout, view = self)
                await user.send("🕒 Die Zeit ist abgelaufen, falls du doch spielen willst schicke eine neue Anfrage!")
                await response(msg.author, user, 2)

            @dc.ui.button(label="Akzeptieren", style = dc.ButtonStyle.green)
            async def button_accept_callback(self, button, interaction):
                
                self.disable_all_items()
                await interaction.response.send_message("🎉 Du hast das Quiz akzeptiert!", ephemeral=True)
                await self.message.edit(view=self)
                await response(msg.author, user, 0)
                self.stop()
            
            @dc.ui.button(label="Ablehnen", style = dc.ButtonStyle.red)
            async def button_reject_callback(self, button, interaction):

                self.disable_all_items()
                await interaction.response.send_message("❌ Du hast das Quiz abgelehnt!", ephemeral=True)
                await self.message.edit(view=self)
                await response(msg.author, user, 1)
                self.stop()
        
        embed_timeout = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x597E8D)
        embed_timeout.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)


        embed = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x0099E1)
        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)

        view = Myview()
        try:
            sent_message = await user.send(embed=embed, view=view)
        except dc.Forbidden:
            msg.author.send("Der Nutzer ist nicht erreichbar, da er vermutlich keine Dms akzeptiert.")
            return
        view.message = sent_message
        await view.wait()

    except:
        await msg.channel.send(f"{user.mention} konnte nicht gefunden werden")

async def response(author: dc.Member, user: dc.Member, angenommen):
        
        embed_reject = dc.Embed(title = "❌ Anfrage abgelehnt ❌", description = (f"{user.mention} hat die Anfrage abgelehnt.\n"), color = 0xF93A2F)
        embed_reject.set_author(name=user.display_name, icon_url= user.avatar.url)

        embed_accept = dc.Embed(title= "✅ Anfrage angenommen✅", description = (f"{user.mention} hat die Anfrage abgelehnt.\n"), color = 0x00D166)
        embed_accept.set_author(name=user.display_name, icon_url = user.avatar.url)

        embed_timeout = dc.Embed(title = "🕒 Nicht auf Anfrage reagiert (Timeout) 🕒", description = (f"{user.mention} hat nicht auf die Anfrage reagiert (Timeout).\n" "Versuche die Anfrage erneut zu senden \noder den Nutzer anders zu erreichen\n"), color = 0x597E8D)
        embed_timeout.set_author(name = user.display_name, icon_url = user.avatar.url)

        if angenommen == 0:
            await author.send(embed = embed_accept)   
        elif angenommen == 1: 
            await author.send(embed = embed_reject)  
        else:
            await author.send(embed = embed_timeout)  

bot.run(Token)
