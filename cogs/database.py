import discord 
from discord.ext import commands
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    port = 3000,
    user = "root",
    password = "root",
    database = "main"
)

cursor = db.cursor()


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    
    async def find_questions(self):
        anzahlfragen = self.bot.anzahlfragen

        sql_query = f"""SELECT * FROM FRAGEN 
                WHERE KATERGORIE IN ({self.bot.choosen_kategories}) AND DIFFICULTY IN ({self.bot.choosen_difficulties}) 
                ORDER BY RAND()
                LIMIT {anzahlfragen}
                ;"""

        cursor.execute(sql_query)

        rows = cursor.fetchall()
        return rows


async def setup(bot):
    await bot.add_cog(Database(bot))