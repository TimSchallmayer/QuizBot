import discord as dc
from discord.ext import commands
from discord.ui import Button
import requests
import json
import time
import os
from dotenv import load_dotenv
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
    await msg.send(f"HI{user.mention}")
    try:
        interacted = False
        class Myview(dc.ui.View): 

            def __init__(self): 
                super().__init__(timeout=120)
                self.interacted = False
                self.message = None

            async def on_timeout(self):
                self.disable_all_items()
                await self.message.edit(embed=embed_timeout, view=self)

            @dc.ui.button(label="Akzeptieren", style = dc.ButtonStyle.green)
            async def button_accept_callback(self, button, interaction):

                self.interacted = True
                self.disable_all_items()
                await interaction.response.send_message("🎉 Du hast das Quiz akzeptiert!", ephemeral=True)
                await self.message.edit(view=self)
                self.stop()
            
            @dc.ui.button(label="Ablehnen", style = dc.ButtonStyle.red)
            async def button_reject_callback(self, button, interaction):

                self.interacted = True
                self.disable_all_items()
                await interaction.response.send_message("❌ Du hast das Quiz abgelehnt!", ephemeral=True)
                await self.message.edit(view=self)
                self.stop()
        
        embed_timeout = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Die Zeit ist abgelaufen. Sende eine neue Anfrage um ein Quiz zu starten!\n"
        ), color = 0x00D166)
        embed_timeout.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)


        embed = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x00D166)
        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)

        view = Myview()
        sent_message = await user.send(embed=embed, view=view)
        view.message = sent_message
        await view.wait()

    
    except:
        await msg.channel.send(f"{user.mention} konnte nicht gefunden werden")


bot.run(Token)
