import discord  as dc
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
    
    async def update_user(self, user : dc.Member, punkte: int, wins : int, losses : int, draws : int):
        sql_query = f""" UPDATE Punkte_system SET punkte = punkte + {punkte}, wins = wins + {wins}, losses = losses + {losses}, draws = draws + {draws} WHERE user_id = {user.id} """
        cursor.execute(sql_query)
        db.commit()
    
    async def get_user_Information(self, user : dc.Member):
        sql_query = f""" SELECT * FROM Punkte_system WHERE user_id = {user.id}"""
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result

    async def add_user(self, user : dc.Member, punkte: int, wins : int = 0, losses : int = 0, draws : int = 0):
        sql_query = f""" INSERT INTO Punkte_system (user_id, punkte, wins, losses, draws) VALUES ({user.id}, {punkte}, {wins}, {losses}, {draws}) """
        cursor.execute(sql_query)
        db.commit()
    
    async def remove_user(self, user : dc.Member):
        sql_query = f""" DELETE FROM Punkte_system WHERE user_id = {user.id} """
        cursor.execute(sql_query)
        db.commit()
    
    async def get_leaderboard(self, range: int):
        sql_query = f"""SELECT * FROM Punkte_system ORDER BY punkte DESC LIMIT {range}"""
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result
    
    async def does_user_exist(self, user : dc.Member):
        sql_query = f""" SELECT * FROM Punkte_system WHERE user_id = {user.id} """
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            return True

async def setup(bot):
    await bot.add_cog(Punkte(bot))