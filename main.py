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
                self.interacted = True

            async def on_timeout(self):
                await self.message.edit(embed=embed1, view=Myview())

            @dc.ui.button(label="Akzeptieren", style = dc.ButtonStyle.green)
            async def button_accept_callback(self, button, interaction):
                self.interacted = True
                button.disabled = True
                await interaction.response.send_message("🎉 Du hast das Quiz akzeptiert!", ephemeral=True)
            
            @dc.ui.button(label="Ablehnen", style = dc.ButtonStyle.red)
            async def button_reject_callback(self, button, interaction):
                self.interacted = True
                button.disabled = True
                await interaction.response.send_message("❌ Du hast das Quiz abgelehnt!", ephemeral=True)
        
        embed1 = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Die Zeit ist abgelaufen. Sende eine neue Anfrage um ein Quiz zu starten!\n"
        ), color = 0x00D166)
        embed1.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)


        embed = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x00D166)
        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)

        await user.send(embed=embed, view=Myview())

    
    except:
        await msg.channel.send(f"{user.mention} konnte nicht gefunden werden")


bot.run(Token)
