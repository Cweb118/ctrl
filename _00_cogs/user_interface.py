from discord import Interaction
from nextcord import slash_command
from _02_global_dicts import theJar
from nextcord.ext import commands
from nextcord.ext.commands import bot
from .frontend.card_menu import cardMenu
        
guilds = [588095612436742173, 778448646642728991]

class UserInterface(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name='testmenu', guild_ids=guilds)
    async def testMenu(self, interaction: Interaction):
        await cardMenu.show(interaction)

def setup(bot):
    bot.add_cog(UserInterface(bot))
