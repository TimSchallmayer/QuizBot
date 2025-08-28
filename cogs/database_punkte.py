import discord 
from discord.ext import commands
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    port = 2001,
    user = "root",
    password = "root",
    database = "Punkte"
)

cursor = db.cursor()


class Punkte(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    async def update_user():
        sql_query = f""" """
    
    async def get_user_Information():
        sql_query = f""" """

    async def add_user():
        sql_query = f""" """
    
    async def remove_user():
        sql_query = f""" """
    
    async def get_leaderboard():
        sql_query = f""" """
    


async def setup(bot):
    await bot.add_cog(Punkte(bot))