from ssl import Options
import nextcord
from _02_global_dicts import player_dict, district_dict
from nextcord import interactions
from nextcord.ext import commands
from nextcord.ext.commands import bot
from _00_cogs.commands import Commands

bot = None 


class LocationUI(nextcord.ui.View):
    def __init__(self, info):
        super().__init__(timeout=None)
        self.info = info #Dictionary with playerid and interface channel ID. name:UserID, channel:ChannelID
        self.messageID = None
    
    @nextcord.ui.button(label="Play", style=nextcord.ButtonStyle.green)
    async def playCard(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass # code here
        #drop down menu for where to play card (building, district, or other unit)
        #if location, congrats pick the unit
        
        #if unit or building, which one?
        #after choosing that, pick the unit to play

    @nextcord.ui.button(label="Move", style=nextcord.ButtonStyle.green)
    async def move(self, button, interaction):
        locations = player_dict[self.info["name"]].location.paths
        locationsNames = [location.name for location in locations]
        options = []

        for locationName in locationsNames:
            options.append(nextcord.SelectOption(label=locationName))
        class LocationSelect(nextcord.ui.View):
            def __init__(self, info):
                super().__init__(timeout=300)
                self.selection = None
                self.info = info

                if(len(locations) > 25):
                    raise("TOO MANY ADJACENT LOCATIONS")

            @nextcord.ui.select(options = options)
            async def locationSelect(self, select, interaction):
                self.selection = select.values[0]
            
            @nextcord.ui.button(label="Go", style=nextcord.ButtonStyle.green)
            async def go(self, button, interaction):
                player = player_dict[self.info["name"]]
                district = district_dict[self.selection]
                report = district.movePlayer(player)
                embedded = nextcord.Embed(title="test", color=0x00ff00)
                await interaction.edit(content=report, view = None)
            

        await interaction.send(content = "Select a location to move to.", ephemeral = True, delete_after=300, view=LocationSelect(self.info))

    @nextcord.ui.button(label="Interact", style=nextcord.ButtonStyle.green)
    async def interact(self, button, interaction):
        pass # code here
        
    @nextcord.ui.button(label="Show Buildings", style=nextcord.ButtonStyle.green)
    async def showBuildings(self, button, interaction):
        pass # code here

    @nextcord.ui.button(label="Show Units", style=nextcord.ButtonStyle.green)
    async def showUnits(self, button, interaction):
        await interaction.edit(content=player_dict[self.info[str("name")]].location.report())

        
class UserInterface(commands.Cog):
    def __init__(self, bot1):
        global bot
        bot = bot1
        self.interfaceChannels = [] #List of dictionaries with Player IDs and Interface Channel IDs. name:UserID, channel:ChannelID

    async def initializeInterface(self):
        for player in player_dict:
        #If there is a interfaceChannel ID. There may not be one if the game hasn't been initialized yet.
            if type([player.interfaceChannel]) == int:
                self.interfaceChannels.append({"name":player.memberID, "channel":player.interfaceChannel})
    
    @commands.command(name="testloc")
    async def testLocationsUI(self, ctx):
        view = LocationUI({"name":143574434874130432, "channel":925971800020643890})
        message = await ctx.send(" ", view=view)
        view.messageID = message.id

def setup(bot):
    bot.add_cog(UserInterface(bot))