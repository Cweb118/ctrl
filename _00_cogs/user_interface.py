from discord import Interaction
from nextcord import slash_command
from _02_global_dicts import theJar
from nextcord.ext import commands
from nextcord.ext.commands import bot

class UserInterface(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(UserInterface(bot))
