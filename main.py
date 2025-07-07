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

        button_accept = dc.ui.Button(label="Akzeptieren", style = dc.ButtonStyle.green)
        button_reject = dc.ui.Button(label="Ablehnen", style = dc.ButtonStyle.red)

        embed = dc.Embed(title="📩 Quiz-Einladung",
        description=(
            f"Hey! {msg.author.mention} hat dich zu einem Quiz eingeladen!\n\n"
            "**Möchtest du an dem Quiz teilnehmen?** 🎉\n"
            "Du hast 2 Minuten Zeit, dich zu entscheiden.\n"
        ), color = 0x00D166)
        embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar.url)

        interacted = False

        async def button_accept_callback(interaction):
            nonlocal interacted
            interacted = True
            await interaction.ressponse.send_message("🎉 Du hast das Quiz akzeptiert!", ephemeral=True)



        async def button_reject_callback(interaction):
            nonlocal interacted
            interacted = True
            await interaction.ressponse.send_message("❌Du hast das Quiz abgelehnt!", ephemeral=True)
            
        button_accept.callback = button_accept_callback
        button_reject.callback = button_reject_callback
    
        view = dc.ui.View()
        view.add_item(button_accept)
        view.add_item(button_reject)


        await user.send(embed=embed, view=view)
        asyncio.wait(120)
        

    
    except:
        await msg.channel.send(f"{user.mention} konnte nicht gefunden werden")


bot.run(Token)
